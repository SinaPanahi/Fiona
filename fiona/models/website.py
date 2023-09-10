from sqlalchemy import Column, String, DateTime, Text, Integer
from datetime import datetime
from fiona import db

class Website(db.Model):
    __tablename__ = 'website'
    id                          = Column(Integer, primary_key=True, autoincrement=True)
    author                      = Column(String(128), nullable=False, default="Sina Panahimoradkandi")
    name                        = Column(String(128), nullable=False, default='Website Name')
    name_description            = Column(Text, nullable=False, 
                                         default='''This is the name of the website. This name will be displayed on the 
                                         browser tab, privacy policy page and terms of use page and other locations as
                                         needed.''')
    address                     = Column(String(128), nullable=False, default="http://127.0.0.1:5000")
    address_description         = Column(Text, nullable=False, 
                                         default='''Website address is used to enable the website to
                                         generate email activation links. This field is essential for enabling
                                         users to activate their accounts. Please, input your domain name
                                         without a trailing slash like: "https://example.com" not 
                                         "https://example.com/"''')
    # Add about_images here later
    about_content               = Column(Text, nullable=False, default='About Page Content')
    about_description           = Column(Text, nullable=False, 
                                         default='''The text in this field will be displayed on the about page of the website.''')
    privacy_policy_content      = Column(Text, nullable=False, default='Privacy Policy Page Content')
    privacy_policy_description  = Column(Text, nullable=False, 
                                         default='''The text in this field will be displayed on the privacy policy page of the website.''')
    terms_of_use_content        = Column(Text, nullable=False, default='Terms of Use Page Content')
    terms_of_use_description    = Column(Text, nullable=False, 
                                         default='''The text in this field will be displayed on the terms of use page of the website.''')
    since                       = Column(DateTime, nullable=False, default=datetime.utcnow)
       

    def __init__(self):
        pass

    def __repr__(self):
        return f'''<Website('{self.author}', 
                          '{self.name}', 
                          '{self.about_content}', 
                          '{self.about_description}',
                          '{self.privacy_policy_content}', 
                          '{self.privacy_policy_description}',
                          '{self.terms_of_use_content}', 
                          '{self.terms_of_use_description}',
                          '{self.since}',
                          '{self.address},
                          '{self.address_description}')>'''
    