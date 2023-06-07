import yaml
import sys
from yattag import Doc

def lambda_handler(event, context):
    configuration = open("config.yaml").read()
    configuration = yaml.load(configuration, Loader=yaml.FullLoader)
    questions = configuration["Questions"]
    title = configuration['Title'];
    author = configuration['Author'];
    image = configuration['Image'];
    theme = configuration['Theme'];
    
    questionsNames = list()
    for questionIterator in questions:
        questionsNames.append(questionIterator)
    questionsNames.sort()
    
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('header'):
            doc.stag('meta charset="utf-8"')
            doc.stag('meta http-equiv="X-UA-Compatible" content="IE=edge"')
            doc.stag('meta name="viewport" content="width=device-width, initial-scale=1"')
            with tag('style', type="text/css"):
                text('body { Margin: 0 !important; padding: 15px; background-color: #4A4A4A;}')
        with tag('body'):
            with tag('div', style="width: 100%; table-layout: fixed;"):
                with tag('div', style="width: 100%; background-color: #eee; max-width: 670px; Margin: 0 auto;"):
                    # with doc.tag('div', style="font-size: medium;font-weight: bold; font-family: verdana; color:#" + str(theme) + ";"): 
                    #     text(title)
                    #     doc.stag('br')
                    with doc.tag('div', style="font-size: small; font-weight: bold; font-family: verdana;"):
                        # text("by " + author)
                        # doc.stag('br')
                        doc.stag('img', src=image, style=" width: 100%; max-width: 670px; height: auto;")
                        doc.stag('br')
                        doc.stag('br')
                    with tag('form', action = "submitsurvey", style="margin-left: auto; margin-right: auto; width: 70%; "):
                        with tag('div'):
                            for questionName in questionsNames:
                                questionLabel = questions[questionName]['Label']
                                questionType = questions[questionName]['Type']
        
                                #doc.stag('font', size="4", style="font-weight: bold; font-family: verdana; color:#" + str(theme) + ";")    
                                with doc.tag('div',style="font-size: medium;font-weight: bold; font-family: verdana; color:#" + str(theme) + ";"): 
                                    doc.asis(questionLabel)
                                    doc.stag('br')
                                
                                if (questionType == "Text"):
                                    doc.stag('br')
                                    with doc.textarea(name = questionName, style="width: 100%; border-color: #" + str(theme) + "; " , rows="5"):
                                        pass
                                    
                                if (questionType == "ShortText"):  
                                    doc.stag('br')
                                    with doc.textarea(name = questionName, style="width: 100%; border-color: #" + str(theme) + "; " , rows="1"):
                                        pass
                                    
                                if (questionType == "Radio"):
                                    values = questions[questionName]['Values']
                                    # doc.stag('br', style=" display: block; margin: 0 0; content: ""; ")
                                    doc.stag('hr', style="height:2px; visibility:hidden; margin-bottom:-5px;")
                                    # doc.stag('br')
                                    for valueIterator in values:
                                        value = questions[questionName]['Values'][valueIterator]
                                        with doc.tag('div', style="font-size: small; font-weight: normal; font-family: verdana; color:black;"):
                                            doc.input(name = questionName, type = 'radio', value = value, style="border-color: #" + str(theme) + "; ")
                                            text(" "+str(value))
                                            doc.stag('br')
                                        
                                if (questionType == "CheckBox"):
                                    with tag('fieldset',style="border: 0px; padding: 0px; font-size: small; font-weight: normal; font-family: verdana; color:black;"):
                                        values = list(questions[questionName]['Values'])
                                        for valueIterator in values:
                                            value = questions[questionName]['Values'][valueIterator]
                                            field_name = questionName + "_" + "".join([ c if c.isalnum() else "_" for c in value.lower() ])
                                            doc.input(name = field_name, type = 'hidden', value = "0",style="border-color: #" + str(theme) + "; ")
                                            doc.input(name = field_name, id = field_name ,  type = 'checkbox', value = "1", style="border-color: #" + str(theme) + "; ")
                                            text(" "+str(value))
                                            doc.stag('br')
                                    
                                doc.stag('br')
                                doc.stag('br')
                                
                        doc.stag('input', type = "submit", value = "Send!", style="background-color: #ed0056; border-radius: 8px; ;cursor: pointer;margin: 4px 2px 20px; border: none; color: white; font-size: 16px; padding: 15px 62px; margin-left : 30%;")




    htmlResult = doc.getvalue()



    return {
            'statusCode': "200",
            'body': htmlResult,
            'headers': {
                'Content-Type': 'text/html',
            }
        }


