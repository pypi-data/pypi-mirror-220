import functools
import json
import logging
import os

import ruamel.yaml

logger = logging.getLogger(__name__)


def include_configuration(loader, filename_node, include_directory):
    '''
    Given a ruamel.yaml.loader.Loader, a ruamel.yaml.serializer.ScalarNode containing the included
    filename, and an include directory path to search for matching files, load the given YAML
    filename (ignoring the given loader so we can use our own) and return its contents as a data
    structure of nested dicts and lists. If the filename is relative, probe for it within 1. the
    current working directory and 2. the given include directory.

    Raise FileNotFoundError if an included file was not found.
    '''
    include_directories = [os.getcwd(), os.path.abspath(include_directory)]
    include_filename = os.path.expanduser(filename_node.value)

    if not os.path.isabs(include_filename):
        candidate_filenames = [
            os.path.join(directory, include_filename) for directory in include_directories
        ]

        for candidate_filename in candidate_filenames:
            if os.path.exists(candidate_filename):
                include_filename = candidate_filename
                break
        else:
            raise FileNotFoundError(
                f'Could not find include {filename_node.value} at {" or ".join(candidate_filenames)}'
            )

    return load_configuration(include_filename)


def raise_retain_node_error(loader, node):
    '''
    Given a ruamel.yaml.loader.Loader and a YAML node, raise an error about "!retain" usage.

    Raise ValueError if a mapping or sequence node is given, as that indicates that "!retain" was
    used in a configuration file without a merge. In configuration files with a merge, mapping and
    sequence nodes with "!retain" tags are handled by deep_merge_nodes() below.

    Also raise ValueError if a scalar node is given, as "!retain" is not supported on scalar nodes.
    '''
    if isinstance(node, (ruamel.yaml.nodes.MappingNode, ruamel.yaml.nodes.SequenceNode)):
        raise ValueError(
            'The !retain tag may only be used within a configuration file containing a merged !include tag.'
        )

    raise ValueError('The !retain tag may only be used on a YAML mapping or sequence.')


def raise_omit_node_error(loader, node):
    '''
    Given a ruamel.yaml.loader.Loader and a YAML node, raise an error about "!omit" usage.

    Raise ValueError unconditionally, as an "!omit" node here indicates it was used in a
    configuration file without a merge. In configuration files with a merge, nodes with "!omit"
    tags are handled by deep_merge_nodes() below.
    '''
    raise ValueError(
        'The !omit tag may only be used on a scalar (e.g., string) list element within a configuration file containing a merged !include tag.'
    )


class Include_constructor(ruamel.yaml.SafeConstructor):
    '''
    A YAML "constructor" (a ruamel.yaml concept) that supports a custom "!include" tag for including
    separate YAML configuration files. Example syntax: `retention: !include common.yaml`
    '''

    def __init__(self, preserve_quotes=None, loader=None, include_directory=None):
        super(Include_constructor, self).__init__(preserve_quotes, loader)
        self.add_constructor(
            '!include',
            functools.partial(include_configuration, include_directory=include_directory),
        )
        self.add_constructor('!retain', raise_retain_node_error)
        self.add_constructor('!omit', raise_omit_node_error)

    def flatten_mapping(self, node):
        '''
        Support the special case of deep merging included configuration into an existing mapping
        using the YAML '<<' merge key. Example syntax:

        ```
        retention:
            keep_daily: 1

        <<: !include common.yaml
        ```

        These includes are deep merged into the current configuration file. For instance, in this
        example, any "option" with sub-options in common.yaml will get merged into the corresponding
        "option" with sub-options in the example configuration file.
        '''
        representer = ruamel.yaml.representer.SafeRepresenter()

        for index, (key_node, value_node) in enumerate(node.value):
            if key_node.tag == u'tag:yaml.org,2002:merge' and value_node.tag == '!include':
                included_value = representer.represent_data(self.construct_object(value_node))
                node.value[index] = (key_node, included_value)

        super(Include_constructor, self).flatten_mapping(node)

        node.value = deep_merge_nodes(node.value)


def load_configuration(filename):
    '''
    Load the given configuration file and return its contents as a data structure of nested dicts
    and lists. Also, replace any "{constant}" strings with the value of the "constant" key in the
    "constants" option of the configuration file.

    Raise ruamel.yaml.error.YAMLError if something goes wrong parsing the YAML, or RecursionError
    if there are too many recursive includes.
    '''

    # Use an embedded derived class for the include constructor so as to capture the filename
    # value. (functools.partial doesn't work for this use case because yaml.Constructor has to be
    # an actual class.)
    class Include_constructor_with_include_directory(Include_constructor):
        def __init__(self, preserve_quotes=None, loader=None):
            super(Include_constructor_with_include_directory, self).__init__(
                preserve_quotes, loader, include_directory=os.path.dirname(filename)
            )

    yaml = ruamel.yaml.YAML(typ='safe')
    yaml.Constructor = Include_constructor_with_include_directory

    with open(filename) as file:
        file_contents = file.read()
        config = yaml.load(file_contents)

        if config and 'constants' in config:
            for key, value in config['constants'].items():
                value = json.dumps(value)
                file_contents = file_contents.replace(f'{{{key}}}', value.strip('"'))

            config = yaml.load(file_contents)
            del config['constants']

        return config


def filter_omitted_nodes(nodes):
    '''
    Given a list of nodes, return a filtered list omitting any nodes with an "!omit" tag or with a
    value matching such nodes.
    '''
    omitted_values = tuple(node.value for node in nodes if node.tag == '!omit')

    return [node for node in nodes if node.value not in omitted_values]


DELETED_NODE = object()


def deep_merge_nodes(nodes):
    '''
    Given a nested borgmatic configuration data structure as a list of tuples in the form of:

        (
            ruamel.yaml.nodes.ScalarNode as a key,
            ruamel.yaml.nodes.MappingNode or other Node as a value,
        ),

    ... deep merge any node values corresponding to duplicate keys and return the result. If
    there are colliding keys with non-MappingNode values (e.g., integers or strings), the last
    of the values wins.

    For instance, given node values of:

        [
            (
                ScalarNode(tag='tag:yaml.org,2002:str', value='retention'),
                MappingNode(tag='tag:yaml.org,2002:map', value=[
                    (
                        ScalarNode(tag='tag:yaml.org,2002:str', value='keep_hourly'),
                        ScalarNode(tag='tag:yaml.org,2002:int', value='24')
                    ),
                    (
                        ScalarNode(tag='tag:yaml.org,2002:str', value='keep_daily'),
                        ScalarNode(tag='tag:yaml.org,2002:int', value='7')
                    ),
                ]),
            ),
            (
                ScalarNode(tag='tag:yaml.org,2002:str', value='retention'),
                MappingNode(tag='tag:yaml.org,2002:map', value=[
                    (
                        ScalarNode(tag='tag:yaml.org,2002:str', value='keep_daily'),
                        ScalarNode(tag='tag:yaml.org,2002:int', value='5')
                    ),
                ]),
            ),
        ]

    ... the returned result would be:

        [
            (
                ScalarNode(tag='tag:yaml.org,2002:str', value='retention'),
                MappingNode(tag='tag:yaml.org,2002:map', value=[
                    (
                        ScalarNode(tag='tag:yaml.org,2002:str', value='keep_hourly'),
                        ScalarNode(tag='tag:yaml.org,2002:int', value='24')
                    ),
                    (
                        ScalarNode(tag='tag:yaml.org,2002:str', value='keep_daily'),
                        ScalarNode(tag='tag:yaml.org,2002:int', value='5')
                    ),
                ]),
            ),
        ]

    If a mapping or sequence node has a YAML "!retain" tag, then that node is not merged.

    The purpose of deep merging like this is to support, for instance, merging one borgmatic
    configuration file into another for reuse, such that a configuration option with sub-options
    does not completely replace the corresponding option in a merged file.

    Raise ValueError if a merge is implied using two incompatible types.
    '''
    # Map from original node key/value to the replacement merged node. DELETED_NODE as a replacement
    # node indications deletion.
    replaced_nodes = {}

    # To find nodes that require merging, compare each node with each other node.
    for a_key, a_value in nodes:
        for b_key, b_value in nodes:
            # If we've already considered one of the nodes for merging, skip it.
            if (a_key, a_value) in replaced_nodes or (b_key, b_value) in replaced_nodes:
                continue

            # If the keys match and the values are different, we need to merge these two A and B nodes.
            if a_key.tag == b_key.tag and a_key.value == b_key.value and a_value != b_value:
                if not type(a_value) is type(b_value):
                    raise ValueError(
                        f'Incompatible types found when trying to merge "{a_key.value}:" values across configuration files: {type(a_value).id} and {type(b_value).id}'
                    )

                # Since we're merging into the B node, consider the A node a duplicate and remove it.
                replaced_nodes[(a_key, a_value)] = DELETED_NODE

                # If we're dealing with MappingNodes, recurse and merge its values as well.
                if isinstance(b_value, ruamel.yaml.nodes.MappingNode):
                    # A "!retain" tag says to skip deep merging for this node. Replace the tag so
                    # downstream schema validation doesn't break on our application-specific tag.
                    if b_value.tag == '!retain':
                        b_value.tag = 'tag:yaml.org,2002:map'
                    else:
                        replaced_nodes[(b_key, b_value)] = (
                            b_key,
                            ruamel.yaml.nodes.MappingNode(
                                tag=b_value.tag,
                                value=deep_merge_nodes(a_value.value + b_value.value),
                                start_mark=b_value.start_mark,
                                end_mark=b_value.end_mark,
                                flow_style=b_value.flow_style,
                                comment=b_value.comment,
                                anchor=b_value.anchor,
                            ),
                        )
                # If we're dealing with SequenceNodes, merge by appending one sequence to the other.
                elif isinstance(b_value, ruamel.yaml.nodes.SequenceNode):
                    # A "!retain" tag says to skip deep merging for this node. Replace the tag so
                    # downstream schema validation doesn't break on our application-specific tag.
                    if b_value.tag == '!retain':
                        b_value.tag = 'tag:yaml.org,2002:seq'
                    else:
                        replaced_nodes[(b_key, b_value)] = (
                            b_key,
                            ruamel.yaml.nodes.SequenceNode(
                                tag=b_value.tag,
                                value=filter_omitted_nodes(a_value.value + b_value.value),
                                start_mark=b_value.start_mark,
                                end_mark=b_value.end_mark,
                                flow_style=b_value.flow_style,
                                comment=b_value.comment,
                                anchor=b_value.anchor,
                            ),
                        )

    return [
        replaced_nodes.get(node, node) for node in nodes if replaced_nodes.get(node) != DELETED_NODE
    ]
