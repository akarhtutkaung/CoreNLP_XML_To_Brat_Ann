try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import sys
import os.path

def convert_core_nlp_xml_to_brat_ann(input_file_name):
    """
    Converts Core NLP XML to Brat Ann format.

    Args:
        input_file_name (str): The name of the input XML file.

    Returns:
        None
    """
    # Check if the input file exists and has the correct format
    if not input_file_name.endswith(".xml"):
        print("[!] Error: Wrong File Format.")
        print("[!] File: " + input_file_name)
        sys.exit(1)

    if not os.path.exists(input_file_name):
        print("[!] Error: File Does Not Exist.")
        print("[!] File: " + input_file_name)
        sys.exit(1)

    # Get the output file name by replacing the extension of the input file
    output_file_name = input_file_name.replace(".xml", ".ann")

    # Parse the XML file
    tree = ET.ElementTree(file=input_file_name)
    root = tree.getroot()
    doc = root.find('document')
    sentences = doc.find('sentences').findall('sentence')

    # Initialize lists to store the span types, relation types, and visual configurations
    span_types = []
    relation_types = []
    visual_config_initial = []
    visual_config_final = []
    visual = {}

    # Open the output file
    with open(output_file_name, 'w') as output:
        # Initialize the relation type count
        relation_type_count = 1

        # Iterate over each sentence in the XML file
        for sentence in sentences:
            sentence_id = str(sentence.get('id'))

            # Parse POS tags
            tokens = sentence.find('tokens').findall('token')
            for token in tokens:
                token_id = 'T' + sentence_id + str(token.get('id'))
                pos = str(token.find('POS').text)
                start_idx = str(token.find('CharacterOffsetBegin').text)
                end_idx = str(token.find('CharacterOffsetEnd').text)
                word = str(token.find('word').text)

                # Replace special characters in the POS tag
                pos = replace_special_characters(pos, visual_config_initial, visual_config_final)

                # Add the POS tag to the span types list if it's not already there
                if pos not in span_types:
                    span_types.append(pos)

                # Write the token information to the output file
                output.write(token_id + '\t' + pos + ' ' + start_idx + ' ' + end_idx + '\t' + word + '\n')

            # Parse enhanced plus plus relations
            target_dep = None
            for dependency in sentence.findall('dependencies'):
                if dependency.get('type') == 'enhanced-plus-plus-dependencies':
                    target_dep = dependency
                    break

            if target_dep is not None:
                for dep in target_dep:
                    relation_word = str(dep.get('type'))

                    # Skip the root relation
                    if relation_word == "root":
                        continue

                    # Replace special characters in the relation word
                    relation_word = replace_special_characters(relation_word, visual_config_initial, visual_config_final)

                    # Add the relation word to the relation types list if it's not already there
                    if relation_word not in relation_types:
                        relation_types.append(relation_word)

                    # Write the relation information to the output file
                    relation_id = 'R' + str(relation_type_count)
                    relation_type_count += 1
                    governor_idx = dep.find('governor').get('idx')
                    governor = 'T' + sentence_id + str(governor_idx)
                    dependent_idx = dep.find('dependent').get('idx')
                    dependent = 'T' + sentence_id + str(dependent_idx)
                    output.write(relation_id + '\t' + relation_word + ' Arg1:' + governor + ' Arg2:' + dependent + '\n')

    # Write the annotation configuration file
    with open('annotation.conf', 'w') as conf:
        conf.write('[entities]\n')
        for span_type in span_types:
            conf.write(span_type + '\n')
        conf.write('\n[relations]\n')
        for relation_type in relation_types:
            conf.write(relation_type + '\t' + 'Arg1:<ENTITY>,' + '\t' + ' Arg2:<ENTITY>\n')

    # Write the visual configuration file
    with open('visual.conf', 'w') as conf:
        conf.write('[labels]\n')
        for i in range(len(visual_config_initial)):
            conf.write(visual_config_final[i] + " | " + visual_config_initial[i] + "\n")
        conf.write('[drawing]\n')
        conf.write('SPAN_DEFAULT\tfgColor:black, bgColor:lightgreen, borderColor:darken\n')
        conf.write('ARC_DEFAULT\tcolor:black, dashArray:-, arrowHead:triangle-5, labelArrow:none\n')

def replace_special_characters(s, visual_config_initial, visual_config_final):
    """
    Replaces special characters in a string with their corresponding visual configuration.

    Args:
        s (str): The input string.
        visual_config_initial (list): The list of initial visual configurations.
        visual_config_final (list): The list of final visual configurations.

    Returns:
        str: The string with special characters replaced.
    """
    if ":" in s:
        if s not in visual_config_initial:
            visual_config_initial.append(s)
            s = s.replace(":", "_")
            visual_config_final.append(s)
        else:
            s = s.replace(":", "_")
    if "." in s:
        if s not in visual_config_initial:
            visual_config_initial.append(s)
            s = s.replace(".", "_dot")
            visual_config_final.append(s)
        else:
            s = s.replace(".", "_dot")
    if "," in s:
        if s not in visual_config_initial:
            visual_config_initial.append(s)
            s = s.replace(",", "_comma")
            visual_config_final.append(s)
        else:
            s = s.replace(",", "_comma")
    if "$" in s:
        if s not in visual_config_initial:
            visual_config_initial.append(s)
            s = s.replace("$", "_dollar")
            visual_config_final.append(s)
        else:
            s = s.replace("$", "_dollar")
    return s

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 converter.py [fileName.xml]")
        sys.exit(1)

    input_file_name = sys.argv[1]
    convert_core_nlp_xml_to_brat_ann(input_file_name)