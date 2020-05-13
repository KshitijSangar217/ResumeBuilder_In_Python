from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMessage
import smtplib
from email.message import EmailMessage
import imghdr
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re


def home(request):
    print('\n YaY')
    if request.method == "POST":
        global template_loc, tmp, img_h, data
        data = request.POST

        template_loc = "images/ResumeSite.jpg"
        tmp = Image.open(template_loc)  # Cft = Certificate
        linedrw = ImageDraw.Draw(tmp)
        s_size = 15
        m_size = 22

        # Drawing Name ----------------------------------------------------------
        xCrnt, yCrnt = drawtext(data['name'], 50, 35, 41, 30, (255, 255, 255), path="fonts/Righteous-Regular.ttf")

        # Drawing Contacts 478 176 ----------------------------------------------
        font = ImageFont.truetype('arial.ttf', s_size)
        img_h = font.getsize('I')[1]
        xCrnt = 478
        yCrnt = 180
        drawimg('images/email1.png',480,yCrnt)
        xCrnt, yCrnt = drawtext(data['email'], s_size, 25, 510, yCrnt+2, (0, 0, 0))

        drawimg('images/phone1.png', 480, yCrnt+10)
        xCrnt, yCrnt = drawtext(data['number'], s_size, 25, 510, yCrnt+12, (0, 0, 0))

        drawimg('images/maps1.png', 480, yCrnt + 17)
        xCrnt, yCrnt = drawtext(data['address'], s_size, 25, 510, yCrnt+12, (0, 0, 0)) #(53, 63, 88)

        drawimg('images/linkedin1.png', 480, yCrnt + 13)
        xCrnt, yCrnt = drawtext(data['linkedin'], s_size, 25, 510, yCrnt+12, (0, 0, 0))


        # Drawing skills
        xCrnt, yCrnt = drawtext("SKILLS", m_size, 20, 490, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt+10), (xCrnt+50, yCrnt+10)], fill=(97, 115, 159))
        yCrnt += 5
        temp = re.split(",",data['skills'])
        for i in temp:
            xCrnt, yCrnt = drawtext(i, s_size, 25, 490, yCrnt + 8, (0, 0, 0))


        # Drawing Education
        xCrnt, yCrnt = drawtext("EDUCATION", m_size, 20, 490, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        yCrnt += 8
        for i in range(1, 5):
            s = 'school'+ " " + str(i)
            y = 'year' + " " + str(i)
            m = 'marks'+ " " + str(i)

            if(data[s] != ''):
                xCrnt, yCrnt = drawtext(data[s], s_size+3, 20, 490, yCrnt + 18, (0, 0, 0))
                xCrnt, yCrnt = drawtext(data[y] + " / " + data[m], s_size, 25, 490, yCrnt + 5, (0, 0, 0))

        # Drawing Awards
        yCrnt += 5
        xCrnt, yCrnt = drawtext("AWARDS", m_size, 25, xCrnt, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        awards = re.split("\*", data["awards"])
        for i in range(0, len(awards)):
            xCrnt, yCrnt = drawtext(awards[i], s_size, 30, xCrnt, yCrnt + 8, (0, 0, 0))

        # Drawing Summary
        xCrnt = 41
        yCrnt = 180
        xCrnt, yCrnt = drawtext("SUMMARY", m_size, 25, xCrnt, yCrnt, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        xCrnt, yCrnt = drawtext(data['summary'], s_size, 60, xCrnt, yCrnt + 20, (0, 0, 0))

        # Drawing Experience
        xCrnt, yCrnt = drawtext("EXPERIENCE", m_size, 25, xCrnt, yCrnt + 20, (0, 0, 0))
        linedrw.line([(xCrnt, yCrnt + 10), (xCrnt + 50, yCrnt + 10)], fill=(97, 115, 159))
        experience = re.split("\#|\*", data["experience"])

        for i in range(0, len(experience)):
            xCrnt = 41
            t = 15
            if i == 0:
                t = 25
            if (i % 2) != 0:  # Even
                if i == len(experience)-1:
                    xCrnt, yCrnt = drawtext(experience[i], s_size + 4, 50, xCrnt, yCrnt + t, (0, 0, 0), 1)
                else:
                    xCrnt, yCrnt = drawtext(experience[i], s_size + 4, 50, xCrnt, yCrnt + t, (0, 0, 0))
            else:
                if i == len(experience)-1:
                    xCrnt, yCrnt = drawtext(experience[i], s_size, 50, xCrnt, yCrnt + 6, (0, 0, 0), 1)
                else:
                    xCrnt, yCrnt = drawtext(experience[i], s_size, 50, xCrnt, yCrnt + 6, (0, 0, 0))

        return render(request, "file_sent.html")
    return render(request, "home.html")


def drawimg(loc1, x, y):
    img = Image.open(loc1).resize((img_h + 8, img_h + 8)).convert("L")
    tmp.paste(img, (x, y))


def drawtext(text,size,nwords,x,y, fontcolor, print=0,path='arial.ttf'):

    # --------------------- Making the Resume ---------------------
    # Wrapping the text
    draw = ImageDraw.Draw(tmp)
    font = ImageFont.truetype(path, size)
    lines = textwrap.wrap(text, nwords)

    for line in lines:
        w, h = font.getsize(line)
        draw.text(xy=(x, y), text=line, fill=fontcolor, font=font)
        y = y + h + 6

    if print:
        tmp.show()
        tmp.save('user_resume/Resume_' + str(data["name"].replace(" ", "")) + '.pdf')

        #  Variable Initialization
        filename = 'user_resume/Resume_' + str(data["name"].replace(" ", "")) + '.pdf'
        gmail_id = settings.EMAIL_HOST_USER
        gmail_subject = 'Resume: By Kshitij Sangar'
        gmail_content = """
Hello <name>, 

It's wonderful that you chose this service to make your resume. Good luck for your interview.
        
Regards,
Kshitij Sangar
"""

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()  # Traffic encryption
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        msg = EmailMessage()
        msg['Subject'] = gmail_subject
        msg['From'] = gmail_id
        msg['To'] = data['email']
        gmail_content = gmail_content.replace("<name>", data['name'])
        msg.set_content(gmail_content)

        # Attaching the Poster
        f = open(filename, 'rb')
        fdata = f.read()
        # fname = 'images/' + CertificateFileName
        fname = 'Resume_' + str(data["name"].replace(" ", "")) + '.pdf'

        file_type = imghdr.what(f.name)
        msg.add_attachment(fdata, maintype='application', subtype='octet-stream', filename=fname)
        s.send_message(msg)
        s.quit()

    return x, y
