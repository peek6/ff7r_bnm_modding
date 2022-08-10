import json
import numpy as np
import decimal
import os

#######################
# USAGE
######################

'''
In "USER PARAMETERS" section below, specify:
  1) the src and target JSON (the target will be hacked to include items from the src).
  2) the string to search for when analyzing the JSON (so something like 'Hair' or 'Skirt'
  3) the mapping function to use.  Currently "HAIR" and "SKIRT" are supported.  

Known Issues:  
  Although the script runs and the hacked JSON works in-game after conversion to UASSET/UEXP, 
  and while the original unmodified physics from the target is still working properly, 
  the imported (hacked) physics isn't working properly yet.  
  So, for example, if mapping HAIR from src PC0003_00_BNM to target PC0003_03_BNM, the 
  skirt physics works, but the hair physics is still broken.
'''


########################
## USER PARAMETERS
########################


# to put hair from std into sexy BNM:
src_json = 'PC0003_00_BNM.json'
target_json = 'PC0003_03_BNM.json'
search_for = 'Hair'
to_map = 'HAIR'


'''
# to put skirt from sexy into std BNM:
src_json = 'PC0003_03_BNM.json'
target_json = 'PC0003_00_BNM.json'
search_for = 'Skirt'
to_map = 'SKIRT'
'''

######################
## FUNCTIONS
######################

# add num_indices continuous indices to existing map, starting from src_start_index in the src and from dest_start_idx in the target
# dictionary equivalent of dict[src_start_index:src_start_index+num_indices+1] = np.arange(dest_start_index:(dest_start_index+1))
def append_to_map(dict_in, src_start_index, dest_start_idx, num_indices):
    dict_out = dict_in
    cnt = dest_start_idx
    for idx in range(src_start_index, src_start_index+num_indices):
        dict_out[idx] = cnt
        cnt = cnt+1
    return dict_out

# Based on analysis, define the mappings from the src json to the target json.
# Returns dictionaries (group_mappings, bodies_mappings, links_mappings)
# I am doing this as dictionaries since I want it to throw an error if I try to access non-mapped index
def skirt_mappings():
    # m_Solver mappings
    group_mappings = {} #-1 * np.ones(35, dtype=np.int32)
    #group_indices_to_port = [2, 3, 15, 18, 19, 33, 34]
    group_mappings[1] = 10
    group_mappings[4] = 6
    group_mappings[10] = 20
    group_mappings[11] = 21
    group_mappings[12] = 22
    group_mappings[13] = 23
    group_mappings[14] = 24
    group_mappings[15] = 25

    # m_Bodies mappings
    bodies_mappings = {} #-1 * np.ones(44 + 262, dtype=np.int32)
    bodies_mappings = append_to_map(bodies_mappings, 141, 174, 9) # C_SkirtA

    bodies_mappings = append_to_map(bodies_mappings, 150, 184, 9) # L_SkirtC
    bodies_mappings = append_to_map(bodies_mappings, 159, 154, 6) # L_SkirtD
    bodies_mappings = append_to_map(bodies_mappings, 165, 45, 9) # TODO: There is no std L_SkirtE. Use A.
    bodies_mappings = append_to_map(bodies_mappings, 174, 142, 9) # TODO: There is no std L_SkirtF. Use B

    bodies_mappings = append_to_map(bodies_mappings, 183, 25, 9) # C_SkirtB

    bodies_mappings = append_to_map(bodies_mappings, 219, 132, 9) # R_SkirtC
    bodies_mappings = append_to_map(bodies_mappings, 210, 164, 9)  # R_SkirtD
    bodies_mappings = append_to_map(bodies_mappings, 201, 35, 9)  # TODO:  Again doing R_SxySkirtE -> R_SkirtA
    bodies_mappings = append_to_map(bodies_mappings, 192, 13, 9)  # TODO:  Again doing R_SxySkirtE -> R_SkirtB


    # m_Links mappings
    links_mappings = {}  #TODO:  I will just map onto first 147 skirt-related links for now
    links_mappings = append_to_map(links_mappings, 68, 1, 72)
    links_mappings = append_to_map(links_mappings, 140, 161, 75)

    return (group_mappings, bodies_mappings, links_mappings)


# Based on analysis, define the mappings from the src json to the target json.
# Returns dictionaries (group_mappings, bodies_mappings, links_mappings)
# I am doing this as dictionaries since I want it to throw an error if I try to access non-mapped index
def hair_mappings():

    # Based on analysis, I will try these mappings:

    # m_Solver mappings
    group_mappings = {} #-1 * np.ones(35, dtype=np.int32)
    #group_indices_to_port = [2, 3, 15, 18, 19, 33, 34]
    group_mappings[3] = 3
    group_mappings[33] = 21
    group_mappings[34] = 22
    group_mappings[15] = 6
    group_mappings[18] = 8
    group_mappings[19] = 9

    # TODO:  I am missing groups 2 and 12.
    # For group 12, I will use unused ribbon group 7
    group_mappings[12] = 7
    # For group 2, I will map to group 23 (SxyHair_L)
    group_mappings[2] = 23



    '''
    group_mappings[2] = 3
    group_mappings[3] = 7
    group_mappings[15] = 6
    group_mappings[18] = 8
    group_mappings[19] = 9
    group_mappings[33] = 21
    group_mappings[34] = 22
    '''


    # m_Bodies mappings
    bodies_mappings = {} #-1 * np.ones(44 + 262, dtype=np.int32)

    # C_HairB (285:294) should map to SxyBackHair (111:120)
    bodies_mappings = append_to_map(bodies_mappings, 285, 111, 10)

    # L_HairA -> L_DrsHairA
    bodies_mappings = append_to_map(bodies_mappings, 265, 40, 4)

    # R_HairA -> R_DrsHairA
    bodies_mappings = append_to_map(bodies_mappings, 269, 50, 4)

    # L_HairB -> L_DrsHairB
    # bodies_mappings = append_to_map(bodies_mappings, 298, 40, 4)

    # R_HairB -> R_DrsHairB
    bodies_mappings = append_to_map(bodies_mappings, 302, 55, 4)

    # L_HairC -> L_DrsHairC
    # bodies_mappings = append_to_map(bodies_mappings, 273, 40, 6)

    # R_HairC -> R_DrsHairC
    bodies_mappings = append_to_map(bodies_mappings, 279, 60, 5)  # TODO:  what about _f?

    # L_HairD -> L_DrsHairD
    bodies_mappings = append_to_map(bodies_mappings, 262, 44, 3)

    # R_HairD -> R_DrsHairD
    bodies_mappings = append_to_map(bodies_mappings, 295, 65, 3)

    # TODO:  There is no L_DrsHairB or L_DrsHairC in the SexyDress file.  For now I will use unused L_SexyBackHair bodies to get those 10 items mapped
    # L_HairB -> L_SxyBackHair (a->d)
    bodies_mappings = append_to_map(bodies_mappings, 298, 121, 4)
    # L_HairC -> L_SxyBackHair (e->i) and R_SxyBackHair_a
    bodies_mappings = append_to_map(bodies_mappings, 273, 125, 6)

    #TODO: there are only 5 R_DrsHairC, but there are 6 R_HairC.  Use R_DrsHairD_f (idx 70)
    bodies_mappings[284] = 70

    #TODO:  I will copy the head bodies 256:261, which touch hair, from std into the unused Ribbon slots.  Not sure how this will mesh with existing Head in Sexy
    bodies_mappings = append_to_map(bodies_mappings, 256, 239, 6)


    # m_Links mappings
    links_mappings = {} # -1 * np.ones(42 + 276, dtype=np.int32)

    # C_Hair to C_SxyBackHair
    links_mappings = append_to_map(links_mappings, 301, 41, 9)

    # L_HairA
    links_mappings = append_to_map(links_mappings, 280, 4, 3)
    links_mappings = append_to_map(links_mappings, 283, 237, 2) # TODO:  not enough.  use last 2 ribbon for now.

    # TODO: need to find mappings for L_HairB and C.  Using Sxy for now
    links_mappings = append_to_map(links_mappings, 312, 50, 3)
    links_mappings = append_to_map(links_mappings, 290, 53, 5)

    # L_HairD
    links_mappings = append_to_map(links_mappings, 278, 7, 2)

    # R_HairA
    links_mappings = append_to_map(links_mappings, 285, 12, 4)
    links_mappings[289] = 59 # TODO:  not enough.  USe R_SxyBackHair_a for now
    links_mappings = append_to_map(links_mappings, 315, 16, 3) # B
    links_mappings = append_to_map(links_mappings, 295, 23, 6) # C
    links_mappings = append_to_map(links_mappings, 310, 30, 2) # D

    # TODO:  Head.  Use Ribbon for now
    links_mappings = append_to_map(links_mappings, 276, 235, 2)



    return (group_mappings, bodies_mappings, links_mappings)

# As a simple test, try only mapping the back hair
def back_hair_mappings():

    # Based on analysis, I will try these mappings:

    # m_Solver mappings
    group_mappings = {} #-1 * np.ones(35, dtype=np.int32)
    # Back hair in both uses group ID 3
    group_mappings[3] = 3
    '''
    group_mappings[2] = 3
    group_mappings[3] = 7
    group_mappings[15] = 6
    group_mappings[18] = 8
    group_mappings[19] = 9
    group_mappings[33] = 21
    group_mappings[34] = 22
    '''

    # m_Bodies mappings
    bodies_mappings = {} #-1 * np.ones(44 + 262, dtype=np.int32)
    bodies_mappings = append_to_map(bodies_mappings, 285, 111, 10)


    # m_Links mappings
    links_mappings = {}
    links_mappings = append_to_map(links_mappings, 301, 41, 9)

    return (group_mappings, bodies_mappings, links_mappings)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, decimal.Decimal):
            return "REMOVE_QUOTE"+str(obj)+"REMOVE_QUOTE" #f'{obj.normalize():f}'
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

# Analyze the BNM JSON and print indices relating to string_to_search (e.g., something like 'Hair' or 'Skirt')
def analyze_json(json_filename, string_to_search):

    # some JSON:
    json_f = open(json_filename)

    # parse json files:
    dict_to_parse = json.load(json_f, parse_float=decimal.Decimal)

    out_str = ''

    my_root = dict_to_parse['Exports'][0]['Data']

    bnm_types_range = range(len(my_root))
    for idx_bnm_type in bnm_types_range:

        if(isinstance(my_root[idx_bnm_type]['Value'], list)):
            out_str = out_str+'Printing out values for BNM index ' + str(idx_bnm_type) + ', BNM type ' + my_root[idx_bnm_type]['Name'] + ':' + '\n'
            item_range = range(len(my_root[idx_bnm_type]['Value']))
            relevant_cnt = 0
            for item_idx in item_range:

                found_parent_id = False
                found_child_id = False
                found_group_id = False
                found_idx = False
                found_group_name = False
                found_joint_name = False
                found_parent_name = False
                found_child_name = False
                found_target_string = False

                if (isinstance(my_root[idx_bnm_type]['Value'][item_idx],dict)):
                 if('Value' in my_root[idx_bnm_type]['Value'][item_idx].keys()):
                   if(isinstance(my_root[idx_bnm_type]['Value'][item_idx]['Value'], list)):
                    property_range = range(len(my_root[idx_bnm_type]['Value'][item_idx]['Value']))

                    for property_idx in property_range:

                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name']=='m_ParentId'):
                            parent_id = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            assert(found_parent_id == False)
                            found_parent_id = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_ChildId'):
                            assert(found_child_id == False)
                            child_id = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            found_child_id = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_GroupId'):
                            group_id = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            found_group_id = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_Index'):
                            index = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            found_idx = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_GroupName'):
                            group_name = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            found_group_name = True
                            if(group_name != None and string_to_search in group_name):
                                found_target_string = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_JointName'):
                            joint_name = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            found_joint_name = True
                            if(joint_name != None and string_to_search in joint_name):
                                found_target_string = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_ParentBodyName'):
                            parent_name = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            assert(found_parent_name == False)
                            found_parent_name = True
                            if(parent_name != None and string_to_search in parent_name):
                                found_target_string = True
                        if (my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name'] == 'm_ChildBodyName'):
                            child_name = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            assert(found_child_name == False)
                            found_child_name = True
                            if(child_name != None and string_to_search in child_name):
                                found_target_string = True

                        # does the string ever show up in something that is not a parent, child, group, or joint?
                        if('Value' in my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx].keys()):
                            val = my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Value']
                            if(isinstance(val,str) and string_to_search in val):
                                if(found_target_string==False):
                                    out_str = out_str + "WARNING: Found "+string_to_search+" in unexpected type "+my_root[idx_bnm_type]['Value'][item_idx]['Value'][property_idx]['Name']
                                found_target_string = True



                if found_target_string==True:
                    relevant_cnt = relevant_cnt + 1
                    if(found_idx==True):
                        assert (item_idx == index)
                    out_str = out_str + 'Index ' + str(item_idx)+': '
                    if(found_group_id==True):
                        out_str = out_str + 'Group ID: ' + str(group_id) + ', '
                    if(found_joint_name==True):
                        out_str = out_str + 'Joint: ' + joint_name + ', '
                    if(found_group_name==True):
                        out_str = out_str +  'Group: ' + group_name + ', '
                    if (found_parent_name==True and parent_name!=None):
                        out_str = out_str + 'Parent: {' + str(parent_id) + ': ' + parent_name + '}, '
                    if (found_child_name==True and child_name!=None):
                        out_str = out_str + 'Child: {' + str(child_id) + ': ' + child_name + '}'
                    out_str = out_str + '\n'


            out_str = out_str + string_to_search + ' Nodes: ' + str(relevant_cnt) + '\n'

    # Write results of analysis to file
    with open(string_to_search+'_references_in_'+os.path.splitext(json_filename)[0]+'.txt', 'w') as file:
        file.write(out_str)

    return my_root


# Creates a hacked version of the dest JSON file prefixed by hacked_, which contains the items from the src JSON file as specified in the mappings
def hack_json(src_filename, dest_filename, group_mappings, bodies_mappings, links_mappings):

    # Both files have solvers, bodies, links in 2,3,4, respectively:
    solver_json_index = 2
    body_json_index = 3
    link_json_index = 4

    src_json_f = open(src_filename)
    dest_json_f = open(dest_filename)

    # parse json files:
    src_dict = json.load(src_json_f,parse_float=decimal.Decimal)
    dest_dict = json.load(dest_json_f,parse_float=decimal.Decimal)

    src_root = src_dict['Exports'][0]['Data']

    for solver_idx in group_mappings.keys():
        # Put solver in src[solver_idx] into dest[solver_idx]
        dest_dict['Exports'][0]['Data'][solver_json_index]['Value'][group_mappings[solver_idx]] = src_root[solver_json_index]['Value'][solver_idx]
        # Hack the group ID
        dest_dict['Exports'][0]['Data'][solver_json_index]['Value'][group_mappings[solver_idx]]['Value'][0]['Value'] = int(group_mappings[solver_idx])

    # Bodies
    for body_idx in bodies_mappings.keys():
        #print('Processing Body Idx: ', body_idx)
        # Put body in src[body_idx] into dest[body_idx]
        dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]] = src_root[body_json_index]['Value'][body_idx]
        # Hack the joint ID
        dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][0]['Value'] = int(bodies_mappings[body_idx])
        # Hack the parent ID
        if(dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][2]['Value']  != None):
            src_parent_idx = src_root[body_json_index]['Value'][body_idx]['Value'][4]['Value']
            #print('src_parent_idx=', src_parent_idx)
            dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][4]['Value'] = int(bodies_mappings[src_parent_idx])
        # Hack the child ID
        if(dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][3]['Value']  != None):
            src_child_idx = src_root[body_json_index]['Value'][body_idx]['Value'][5]['Value']
            #print('src_child_idx=', src_child_idx)
            dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][5]['Value'] = int(bodies_mappings[src_child_idx])
        # Hack the group ID
        dest_dict['Exports'][0]['Data'][body_json_index]['Value'][bodies_mappings[body_idx]]['Value'][6]['Value']  = int(group_mappings[src_root[body_json_index]['Value'][body_idx]['Value'][6]['Value'] ])


    # Links
    for link_idx in links_mappings.keys():
        #print('Processing Link Idx: ', link_idx)
        # Put link in src[link_idx] into dest[link_idx]
        dest_dict['Exports'][0]['Data'][link_json_index]['Value'][links_mappings[link_idx]] = src_root[link_json_index]['Value'][link_idx]

        # Hack the parent ID
        src_parent_idx = src_root[link_json_index]['Value'][link_idx]['Value'][2]['Value']
        if(src_parent_idx in bodies_mappings.keys()):
            dest_dict['Exports'][0]['Data'][link_json_index]['Value'][links_mappings[link_idx]]['Value'][2]['Value'] = int(bodies_mappings[src_parent_idx])
        else:
            print('Warning:  in link index ', str(link_idx),': Parent Idx ',src_parent_idx,' links to desired body part but was not mapped.')


        # Hack the child ID
        src_child_idx = src_root[link_json_index]['Value'][link_idx]['Value'][3]['Value']
        if(src_child_idx in bodies_mappings.keys()):
            dest_dict['Exports'][0]['Data'][link_json_index]['Value'][links_mappings[link_idx]]['Value'][3]['Value'] = int(bodies_mappings[src_child_idx])
        else:
            print('Warning in link index ', str(link_idx),': Child Idx ',src_child_idx,' links to desired body part but was not mapped.')


    # print the hacked dest dict to a file
    with open('hacked_'+dest_filename,'w') as f:
        json.dump(dest_dict, f, indent=2, cls=DecimalEncoder)


    # There is a precision issue where reading in values as Python float loses precision
    # Instead, I read them in as decimal.Decimal to keep precision, but then JSON dump serializer can't write them out
    # As a workaround, I convert to strings, which makes the JSON encoder stick "" around the floats
    # I put the string REMOVE_QUOTE around quotes I want to later remove, and am removing them here:

    with open('hacked_'+dest_filename, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\"REMOVE_QUOTE', '')
    filedata = filedata.replace('REMOVE_QUOTE\"', '')


    # Write the file out again
    with open('hacked_'+dest_filename, 'w') as file:
        file.write(filedata)

    return dest_dict


###################################
#  MAIN ENTRY POINT
###################################

# Run analysis on the 2 JSON files:
src_exports_dict = analyze_json(src_json, search_for)
target_exports_dict = analyze_json(target_json, search_for)

# Pick the desired mapping
if to_map == 'HAIR':
    (group_mappings, bodies_mappings, links_mappings) = hair_mappings()
else:
    if to_map == 'SKIRT':
        (group_mappings, bodies_mappings, links_mappings) = skirt_mappings()
    else:
        print('WARNING:  invalid mapping type selected.  No hacking will be done.')
        group_mappings = {}
        bodies_mappings = {}
        links_mappings = {}


hacked_dict = hack_json(src_json, target_json, group_mappings, bodies_mappings, links_mappings)
