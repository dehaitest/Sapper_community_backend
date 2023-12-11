# app/common/data_conversion.py

def convert_spl_to_splform(spl): 
    splform = {"formData": []}
    for section_type, sections in spl.items():
        section_id = str(len(splform['formData']))
        if 'Instruction' in section_type:
            print(sections.items())
            splform_sections = [{"subSectionId": str(i), "sequencialId": key.split('-')[1], "subSectionType": key.split('-')[0], "content": value} for i, (key, value) in enumerate(sections.items())]
            splform['formData'].append({"sectionId": section_id, "sectionType": section_type, "sections": splform_sections})
        elif 'Guardrails' in section_type:
            splform_sections = [{"subSectionId": str(i), "subSectionType": key, "content": value} for i, (key, value) in enumerate(sections.items())]
            splform['formData'].append({"sectionId": section_id, "sectionType": "Guardrails", "sections": splform_sections})
        else:
            splform_sections = [{"subSectionId": sec.split('-')[1], "subSectionType": sec.split('-')[0], "content": value} for sec, value in sections.items()]
            splform['formData'].append({"sectionId": section_id, "sectionType": section_type, "sections": splform_sections})
    return splform      

def convert_splform_to_spl(splform):
    spl = {}
    i = 0
    for section in splform['formData']:
        if section['sectionType'] == "Instruction":
            section_key = f"{section['sectionType']}-{i}" 
            i += 1
            spl[section_key] = {}
            for sub_section in section['sections']:
                sub_section_key = f"{sub_section['subSectionType']}-{sub_section['sequencialId']}"
                spl[section_key][sub_section_key] = sub_section['content']
        elif section['sectionType'] == "Guardrails":
            section_key = section['sectionType']
            spl[section_key] = {}
            for sub_section in section['sections']:
                spl[section_key][sub_section['subSectionType']] = sub_section['content']
        else:
            section_key = section['sectionType']
            spl[section_key] = {}
            for sub_section in section['sections']:
                sub_section_key = f"{sub_section['subSectionType']}-{sub_section['subSectionId']}"
                spl[section_key][sub_section_key] = sub_section['content']
    return spl
