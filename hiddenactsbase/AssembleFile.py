import os

from django.forms import model_to_dict
from docx import Document
from docxtpl import DocxTemplate


def _doc_append(file1, file2):
    doc1 = Document(file1)
    doc2 = Document(file2)
    for el in doc2.element.body:
        doc1.element.body.append(el)
    doc1.save(file1)


def _make_hidden_docx(obj, docx_template_name, dynamic_dir_name, additional_acts_templates, prefix,
                      only_additional_acts=False):
    i = 1
    if not only_additional_acts:
        for act in obj.acts.all():
            context = model_to_dict(obj, exclude=['id', 'acts'])
            context.update(model_to_dict(act, exclude=['id']))
            name = prefix + '-' + str(i)
            doc = DocxTemplate(docx_template_name)
            doc.render(context)
            doc.save(os.path.join(dynamic_dir_name, name + ".docx"))
            i += 1
            context.clear()
    for additional_act_template in additional_acts_templates:
        context = model_to_dict(obj, exclude=['id', 'acts'])
        name = prefix + '-' + str(i)
        doc = DocxTemplate(additional_act_template)
        doc.render(context)
        doc.save(os.path.join(dynamic_dir_name, name + ".docx"))
        i += 1
        context.clear()
    return i - 1


def _assemble_docx(dynamic_dir_name, num_of_docx, prefix):
    result_docx_name = os.path.join(dynamic_dir_name, prefix + '-' + 'result.docx')
    if os.path.exists(result_docx_name):
        os.remove(result_docx_name)
    if os.path.exists(os.path.join(dynamic_dir_name, prefix + '-' + '1.docx')):
        os.rename(os.path.join(dynamic_dir_name, prefix + '-' + '1.docx'), result_docx_name)
    if num_of_docx > 1:
        for i in range(2, num_of_docx + 1):
            _doc_append(result_docx_name,
                       os.path.join(dynamic_dir_name, prefix + '-' + str(i) + '.docx'))
            os.remove(os.path.join(dynamic_dir_name, prefix + '-' + str(i) + '.docx'))
    return result_docx_name


def AssembleFile(obj, user_name, only_additional_acts=False):
    AOSR_template_name = 'HiddenActTemtplate.docx'
    additional_acts_tamplate_names = {
        'is_washing_purging_act': 'WashingPurgingActTemplate.docx',
        'is_washing_disinfection_act': 'WashingDisinfectionActTemplate.docx',
        'is_hydraulic_testing_act': 'HydraulicTestingActTemplate.docx',
        'is_sewer_testing_act': 'SewerTestingActTemplate.docx',
        'is_adjusting_heating_act': 'AdjustmentActTemplate.docx'
    }
    base_app_dir = os.path.dirname(os.path.abspath(__file__))
    dynamic_dir_name = os.path.join(base_app_dir, 'dynamic')
    if not os.path.exists(dynamic_dir_name):
        os.mkdir(dynamic_dir_name)
    docx_template_dir = os.path.join(base_app_dir, 'docx_template')
    AOSR_template = os.path.join(docx_template_dir, AOSR_template_name)
    additional_acts_templates = [os.path.join(docx_template_dir, value)
                                 for (key, value) in additional_acts_tamplate_names.items() if obj.__dict__[key]]

    num_of_docx = _make_hidden_docx(obj, AOSR_template, dynamic_dir_name, additional_acts_templates, user_name,
                                    only_additional_acts)
    docx_name = _assemble_docx(dynamic_dir_name, num_of_docx, user_name)

    return docx_name

