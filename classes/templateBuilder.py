from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText

class Builder:
    def __init__(self):
        return
    
    def build_template(self, symbols, summary, articles, company_name, exchange):
        """
        Takes 5 arguments (symbols [stock symbol arrays], 
        summary [stock article summaries array], 
        articles [array with link to articles mentioning the stocks], 
        company_name [company names array], 
        exchange [exchanges array the stocks belong to]).
        """
        try:
            # Declare jinja2 template
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            template = env.get_template('email.html')
            #build jinja2 template from /templates/email.html
            output = template.render(symbols=symbols, summary=summary, articles=articles, 
                                    companyName=company_name, exchange=exchange)
            body = MIMEText(output, 'html')
            return body
        except Exception as e:
            print(str(e))