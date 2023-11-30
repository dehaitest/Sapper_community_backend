def convert_spl_to_splform(spl):
    splform = {'formData': []}
    for key, value in spl.items():
        splform['formData'].append(
        {"sectionId": str(len(splform['formData'])),
            "sectionType": key,
            "sections": [
                {
                    "subSectionId": str(i),
                    "subSectionType": k,
                    "content": v
                } for i, (k, v) in enumerate(dict(value).items())
            ]
        }) 
    return splform           

def convert_splform_to_spl(splform):
    spl = {}
    for item in splform['formData']:
        spl.update({item["sectionType"]: {section["subSectionType"]: section["content"] for section in item["sections"]}})
    return spl
