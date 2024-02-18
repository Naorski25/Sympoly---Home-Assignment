
class EXRFParser:
    # This function will take a line that is a field type and add it to the desierd blok.
    @staticmethod
    def add_field(line, Blok_dict):
        key, value = line.split("::", 1)
        # Need to check if the key already exists in the dict and if its a leagal key name. --> and return an error if not.
        Blok_dict[key] = value
        return Blok_dict
    
    # This function will get the lines of the file from where a blok starts defines it and adds it to the dict.
    @staticmethod
    def add_blok(lines_in_file, blok_dict):
        blok_name = lines_in_file[0][1:-1]
        #Need to check if the blok name already exists in the dict as a key and if its a leagal key name. --> and return an error if not.
        blok_dict[blok_name] = {}
        line = 1
        while line < len(lines_in_file):
            lines_in_file[line] = lines_in_file[line].strip("\n")
            #In addition to these checks we shuld check for mistakes in the file like a blok that is not closed or a blok that is not opened.
            if (
                lines_in_file[line][0] == lines_in_file[line][1] == ":"
                and lines_in_file[line][-1] == lines_in_file[line][-2] == ":"
                and lines_in_file[line][2:-2] == blok_name
            ):
                break
            else:
                blok_dict[blok_name], lines_to_skip = EXRFParser.exrf_operator(lines_in_file[line:], blok_dict[blok_name])
                line += lines_to_skip - 1 
            line += 1
        return blok_dict, line
    
    # This function will get the lines of the file from where a lists starts defines it and adds it to the blok.
    @staticmethod
    def add_list(lines_in_file, blok_dict):
        list_name = lines_in_file[0][1:-1]
        # Need to check if the list name already exists in the dict as a key and if its a leagal key name. --> and return an error if not.
        blok_dict[list_name] = []
        line = 1
        while line < len(lines_in_file):
            lines_in_file[line] = lines_in_file[line].strip("\n")
            #In addition to these checks we shuld check for mistakes in the file like a list that is not closed or a list that is not opened.
            if (
                lines_in_file[line][0] == lines_in_file[line][1] == "["
                and lines_in_file[line][-1] == lines_in_file[line][-2] == "]"
                and lines_in_file[line][2:-2] == list_name
            ):
                break
            else:
                if lines_in_file[line][0] == "::::":
                    blok_dict[list_name].append({})
                else:
                    blok_dict[list_name], lines_to_skip = EXRFParser.add_blok_to_list(
                        lines_in_file[line:], blok_dict[list_name]
                    )
                    line += lines_to_skip
                line += 1
        return blok_dict, line   
   
    # This function will get the lines of the file from where a lists blok starts defines it and adds it to the list.
    @staticmethod
    def add_blok_to_list(lines_in_file, list_of_bloks):
        blok_dict = {}
        line = 0
        while line < len(lines_in_file):
            lines_in_file[line] = lines_in_file[line].strip()
            #In addition to these checks we shuld check for mistakes in the file like a blok that is not closed or a blok that is not opened.
            if lines_in_file[line] == "::::":
                break
            elif (
                lines_in_file[line][0] in [":", "[", "]"]
                and lines_in_file[line][-1] in [":", "[", "]"]
            ):
                line -= 1
                break
            else:
                blok_dict, lines_to_skip = EXRFParser.exrf_operator(lines_in_file[line:], blok_dict)
                line += lines_to_skip - 1
            line += 1
        list_of_bloks.append(blok_dict)
        return list_of_bloks, line
    
    # This function will take a line and will defind what type of line it is and will call the right function to add it to the dict. 
    @staticmethod
    def exrf_operator(lines_in_file, blok_dict):
        line = 0
        while line < len(lines_in_file):
            lines_in_file[line] = lines_in_file[line].strip("\n")
            if lines_in_file[line] == "":
                break
            else:
                pass
            if (
                lines_in_file[line][0] == lines_in_file[line][-1] == ":"
                and lines_in_file[line][1] != ":"
                and lines_in_file[line][-2] != ":"
            ):
                blok_dict, lines_to_skip = EXRFParser.add_blok(lines_in_file[line:], blok_dict)
                line += lines_to_skip
            elif (
                 lines_in_file[line][0] == "["
                 and lines_in_file[line][1] != "["
                 and lines_in_file[line][-1] == "]"
                 and lines_in_file[line][-2] != "]"
            ):
                blok_dict, lines_to_skip = EXRFParser.add_list(lines_in_file[line:], blok_dict)
                line += lines_to_skip
            elif (
               lines_in_file[line][0] not in [":", "[", "]"]
                and lines_in_file[line][-1] not in [":", "[", "]"]
                and "::" in lines_in_file[line]
                ):
                blok_dict = EXRFParser.add_field(lines_in_file[line], blok_dict)
            else:
                break
            line += 1
        return blok_dict, line
    
    @staticmethod
    def parse_file(file_content: list) -> dict:
        """
        Parse the .exrf file and return the structured data object.
        """
        data_object = {}
        file_content[0] = file_content[0].strip("\n")
        data_object, lines_to_skip = EXRFParser.exrf_operator(file_content, data_object)
        return data_object


