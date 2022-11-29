from django.shortcuts import render,redirect
from django.http import HttpResponse
from pylatex import Document, Package, LongTable, MultiColumn
from pylatex.utils import bold, NoEscape
import mimetypes
import pymongo
import os

def download_page(req):

    client = pymongo.MongoClient()
    dbname = client['capstone']
    filename_collection = dbname['filename']
    pdfs = filename_collection.find({})

    return render(req,"course\downloads.html",
        {
            'pdfs' : pdfs
        })

def download(request,fname):
    filename = f'{fname}.pdf'
    filepath = f"C:\\Users\\DELL\\Desktop\\latex\\syllabus\\{filename}"
    path = open(filepath,'rb')
    mime_type = mimetypes.guess_type(filepath)
    response = HttpResponse(path,content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def edit_page(request,fname):
    client = pymongo.MongoClient()
    dbname = client['capstone']
    filecontent_collection = dbname['filecontent']
    pdf_data = filecontent_collection.find({"filename":fname})
    for data in pdf_data:
        content = data
    num_of_obj = content['num_of_obj']
    num_of_unit = content['num_of_prac']
    num_of_text = content['num_of_text']
    num_of_mooc = content['num_of_mooc']
    num_of_prac = content['num_of_prac']
    num_of_ref = content['num_of_ref']

    objs = []
    units = []
    texts = []
    moocs = []
    pracs = []
    refs = []
    hours = []

    for i in range(0,num_of_obj):
        obj = content[f'objective{i}']
        objs.append(obj)

    for i in range(0,num_of_unit):
        unit = content[f'unit{i}']
        hour = content[f'hour{i}']
        hours.append(hour)
        units.append(unit)
    
    for i in range(0,num_of_text):
        text = content[f'textbook{i}']
        texts.append(text)

    for i in range(0,num_of_mooc):
        mooc = content[f'mooc{i}']
        moocs.append(mooc)

    for i in range(0,num_of_prac):
        prac = content[f'practical{i}']
        pracs.append(prac)

    for i in range(0,num_of_ref):
        ref = content[f'referencebooks{i}']
        refs.append(ref)
 
    return render(request,"course\edit.html",{
        "content" : content,
        "objs" : objs,
        "units" : units,
        "texts" : texts,
        "moocs" : moocs,
        "pracs" : pracs,
        "refs" : refs,
        "hours" : hours
        })
    
def home(request):

    if request.method == "POST":
        un_name = request.POST['un_name']
        faculty_name = request.POST['faculty_name']
        programme = request.POST['programme']
        branch = request.POST['branch']
        semester = request.POST['semester']
        version = request.POST['version']
        effective_academic_year = request.POST['effAY']
        effective_for_batch = request.POST['effBA']
        subject_code = request.POST['subcode']
        # Checking the error for subject code
        if len(subject_code) < 7 or len(subject_code) > 11:
            print("error")
            return render(request,'course/home.html',
            {
                "err" : "incorrect subject code"
            })
        subject_name = request.POST['subname']
        #credits
        lc = request.POST['lc']
        tuc = request.POST['tuc']
        pc = request.POST['pc']
        twc = request.POST['twc']
        totalc = request.POST['totalc']
        #hours
        lh = request.POST['lh']
        tuh = request.POST['tuh']
        ph = request.POST['ph']
        twh = request.POST['twh']
        totalh = request.POST['totalh']
        #theory
        cet = request.POST['cet']
        seet = request.POST['seet']
        totalt = request.POST['totalt']
        #practical
        cep = request.POST['cep']
        seep = request.POST['seep']
        totalp = request.POST['totalp']

        pre_requsites = request.POST['prereq']
        
        #Get all the objectives and add to list
        objectives = []
        num_of_obj = int(request.POST['num_of_obj'])
        for i in range (0,num_of_obj):
            objective = request.POST[f'objective{i}']
            objectives.append(objective)

        #Get units and hrs
        total_hrs = 0
        units = []
        hours = []
        num_of_unit = int(request.POST["num_of_unit"])
        for i in range (0,num_of_unit):
            content = request.POST[f'content{i}']
            hrs = request.POST[f'hrs{i}']
            total_hrs = total_hrs+int(hrs)
            units.append(content)
            hours.append(hrs)

        #Get all practicals and add them to list
        practicals = []
        num_of_prac = int(request.POST['num_of_prac'])
        for i in range (0,num_of_prac):
            practical = request.POST[f'practical{i}']
            practicals.append(practical)

        #Get all textbooks and add them to list
        textbooks = []
        num_of_text = int(request.POST["num_of_text"])
        for i in range(0,num_of_text):
            textbook = request.POST[f'textbook{i}']
            textbooks.append(textbook)

        #Get all referencebooks and add them to list    
        referencebooks = []
        num_of_ref = int(request.POST["num_of_ref"])
        for i in range(0,num_of_ref):
            ref_book = request.POST[f'referencebook{i}']
            referencebooks.append(ref_book)

        #Get all ICT/mooc and add them to list
        Moocs = []
        num_of_mooc = int(request.POST["num_of_mooc"])
        for i in range(0,num_of_mooc):
            mooc = request.POST[f'mooc{i}']
            Moocs.append(mooc)

        #Course Outcomes
        CO1 = request.POST['CO1']
        CO2 = request.POST['CO2']
        CO3 = request.POST['CO3']
        CO4 = request.POST['CO4']
        CO5 = request.POST['CO5']
        CO6 = request.POST['CO6']

        #Course outcomes Mapping

        C1P1 = request.POST['C1P1']
        C1P2 = request.POST['C1P2']
        C1P3 = request.POST['C1P3']
        C1P4 = request.POST['C1P4']
        C1P5 = request.POST['C1P5']
        C1P6 = request.POST['C1P6']
        C1P7 = request.POST['C1P7']
        C1P8 = request.POST['C1P8']
        C1P9 = request.POST['C1P9']
        C1P10 = request.POST['C1P10']
        C1P11 = request.POST['C1P11']
        C1P12 = request.POST['C1P12']
        C1PSO1 = request.POST['C1PSO1']
        C1PSO2 = request.POST['C1PSO2']
        C1PSO3 = request.POST['C1PSO3']

        C2P1 = request.POST['C2P1']
        C2P2 = request.POST['C2P2']
        C2P3 = request.POST['C2P3']
        C2P4 = request.POST['C2P4']
        C2P5 = request.POST['C2P5']
        C2P6 = request.POST['C2P6']
        C2P7 = request.POST['C2P7']
        C2P8 = request.POST['C2P8']
        C2P9 = request.POST['C2P9']
        C2P10 = request.POST['C2P10']
        C2P11 = request.POST['C2P11']
        C2P12 = request.POST['C2P12']
        C2PSO1 = request.POST['C2PSO1']
        C2PSO2 = request.POST['C2PSO2']
        C2PSO3 = request.POST['C2PSO3']

        C3P1 = request.POST['C3P1']
        C3P2 = request.POST['C3P2']
        C3P3 = request.POST['C3P3']
        C3P4 = request.POST['C3P4']
        C3P5 = request.POST['C3P5']
        C3P6 = request.POST['C3P6']
        C3P7 = request.POST['C3P7']
        C3P8 = request.POST['C3P8']
        C3P9 = request.POST['C3P9']
        C3P10 = request.POST['C3P10']
        C3P11 = request.POST['C3P11']
        C3P12 = request.POST['C3P12']
        C3PSO1 = request.POST['C3PSO1']
        C3PSO2 = request.POST['C3PSO2']
        C3PSO3 = request.POST['C3PSO3']

        C4P1 = request.POST['C4P1']
        C4P2 = request.POST['C4P2']
        C4P3 = request.POST['C4P3']
        C4P4 = request.POST['C4P4']
        C4P5 = request.POST['C4P5']
        C4P6 = request.POST['C4P6']
        C4P7 = request.POST['C4P7']
        C4P8 = request.POST['C4P8']
        C4P9 = request.POST['C4P9']
        C4P10 = request.POST['C4P10']
        C4P11 = request.POST['C4P11']
        C4P12 = request.POST['C4P12']
        C4PSO1 = request.POST['C4PSO1']
        C4PSO2 = request.POST['C4PSO2']
        C4PSO3 = request.POST['C4PSO3']

        C5P1 = request.POST['C5P1']
        C5P2 = request.POST['C5P2']
        C5P3 = request.POST['C5P3']
        C5P4 = request.POST['C5P4']
        C5P5 = request.POST['C5P5']
        C5P6 = request.POST['C5P6']
        C5P7 = request.POST['C5P7']
        C5P8 = request.POST['C5P8']
        C5P9 = request.POST['C5P9']
        C5P10 = request.POST['C5P10']
        C5P11 = request.POST['C5P11']
        C5P12 = request.POST['C5P12']
        C5PSO1 = request.POST['C5PSO1']
        C5PSO2 = request.POST['C5PSO2']
        C5PSO3 = request.POST['C5PSO3']

        C6P1 = request.POST['C6P1']
        C6P2 = request.POST['C6P2']
        C6P3 = request.POST['C6P3']
        C6P4 = request.POST['C6P4']
        C6P5 = request.POST['C6P5']
        C6P6 = request.POST['C6P6']
        C6P7 = request.POST['C6P7']
        C6P8 = request.POST['C6P8']
        C6P9 = request.POST['C6P9']
        C6P10 = request.POST['C6P10']
        C6P11 = request.POST['C6P11']
        C6P12 = request.POST['C6P12']
        C6PSO1 = request.POST['C6PSO1']
        C6PSO2 = request.POST['C6PSO2']
        C6PSO3 = request.POST['C6PSO3']

        #Generate the PDF with all the data
        geometry_options = {"top":"0.96cm","right":"2.54cm","bottom":"1.93cm","left":"1.54cm"}
        doc = Document(document_options=["a4paper"],documentclass='article',geometry_options=geometry_options)
        doc.append(NoEscape(r'''\setlength{\tabcolsep}{3.5pt}
                    \centering
                '''))
        doc.packages.append(Package('longtable'))
        doc.packages.append(Package('multirow'))
        doc.packages.append(Package('enumitem'))
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('colortbl'))

        doc.append(NoEscape(r'''\setlength{\tabcolsep}{3.5pt}
                    \centering
                '''))

        with doc.create(LongTable("|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")) as data_table:
            data_table.add_hline()
            data_table.add_row((MultiColumn(16, align='|c|',data= NoEscape(r'\LARGE{')+bold(un_name)+NoEscape(r'}')),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16, align='|c|',data= NoEscape(r'\LARGE{')+bold(faculty_name)+NoEscape(r'}')),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align='|l|',color='black!30',data="Programme"),MultiColumn(5,align='l|',data=programme),
                                MultiColumn(2,align='l|',color="black!30",data="Branch/Spec."),MultiColumn(6,align='l|',data=branch)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align='|l|',color="black!30",data="Semester"),MultiColumn(5,align='l|',data=semester),
                                MultiColumn(2,align='l|',color="black!30",data="Version"),MultiColumn(6,align="l|",data=version)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(5,align="|l|",color="black!30",data="Effective Academic Year"),MultiColumn(3,align="l|",data=effective_academic_year),
                                MultiColumn(5,align="l|",color="black!30",data="Effective for Branch admitted in"),MultiColumn(3,align="l|",data=effective_for_batch)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align="|l|",color="black!30",data="Subject Code"),MultiColumn(3,align="l|",data=subject_code),
                                MultiColumn(2,align='l|',color='black!30',data="Subject Name"),MultiColumn(8,align="l|",data=subject_name)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(8,align="|l|",color="black!30", data="Teaching Scheme"),MultiColumn(8,align="l|",color="black!30",data="Examination Scheme(marks)")))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="per week"),MultiColumn(2,align="l|",data="lecture(DT)"),MultiColumn(2,align="l|",data="Practical(LAB)"),
                                MultiColumn(2,align="l|",data="Total"),MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data="CE"),
                                MultiColumn(2,align="l|",data="SEE"),MultiColumn(2,align="l|",data="Total")),color="black!30")

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data=""),"L","TU","P","TW",MultiColumn(2,align="l|",data=""),
                                MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data=""),
                                MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data="")))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="Credit"),lc,tuc,pc,twc,MultiColumn(2,align="l|",data=totalc),
                                MultiColumn(2,align="l|",data="Theory"),MultiColumn(2,align="l|",data=cet),MultiColumn(2,align="l|",data=seet),MultiColumn(2,align="l|",data=totalt)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="Hours"),lh,tuh,ph,twh,MultiColumn(2,align="l|",data=totalh),
                                MultiColumn(2,align="l|",data="Practicals"),MultiColumn(2,align="l|",data=cep),MultiColumn(2,align="l|",data=seep),MultiColumn(2,align="l|",data=totalp)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Pre-Requsites")),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",data=pre_requsites),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Objective/Learning outcomes of course")),))

            for i in objectives:
                data_table.add_row((MultiColumn(16,align="|l|",data=bold(i)),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align = NoEscape(r"|p{15cm}|"),data=["The educational objectives of course are to educate students to attain the following:"]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|l|',color="black!30",data=bold("Theory Syllabus")),))

            data_table.add_hline()
            data_table.add_row((bold("Unit"),MultiColumn(14,align='c|',data=bold("Content")),bold("Hrs")))

            i = 1
            for j,k in zip(units,hours):
                data_table.add_hline()
                data_table.add_row((bold(i),MultiColumn(14,align=NoEscape(r"|p{14cm}|"),data=j),bold(k)))
                i+=1

            data_table.add_hline()
            data_table.add_row((MultiColumn(15,align='|r|',data="Total"),total_hrs))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|l|',color="black!30",data=bold("Practical content")),))

            for i in practicals:
                data_table.add_row((MultiColumn(16,align='|l|',data=bold(i)),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Text-Books")),))

            i = 0
            for i in range(0,len(textbooks)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=textbooks[i]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Reference Books")),))

            i = 0
            for i in range(0,len(referencebooks)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=referencebooks[i]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("ICT-MOOC reference")),))

            i = 0
            for i in range(0,len(Moocs)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=Moocs[i]),))


            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data="Course Outcomes:"),))

            data_table.add_hline()
            data_table.add_row((bold("COs"),MultiColumn(15,align='|l|',data=bold("Description"))))

            data_table.add_hline()
            data_table.add_row((bold("CO1"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO1)))

            data_table.add_hline()
            data_table.add_row((bold("CO2"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO2)))
            
            data_table.add_hline()
            data_table.add_row((bold("CO3"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO3)))
            
            data_table.add_hline()
            data_table.add_row((bold("CO4"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO4)))

            data_table.add_hline()
            data_table.add_row((bold("CO5"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO5)))

            data_table.add_hline()
            data_table.add_row((bold("CO6"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO6)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|c|',data=bold("Mapping of Co and PO:")),))

            data_table.add_hline()
            data_table.add_row((bold("COs"),bold("PO1"),bold("PO2"),bold("PO3"),bold("PO4"),bold("PO5"),bold("PO6"),bold("PO7"),bold("PO8"),bold("PO9"),bold("PO10"),bold("PO11"),bold("PO12"),bold("PO13"),bold("PO14"),bold("PO15")))

            data_table.add_hline()
            data_table.add_row((bold("CO1"),C1P1,C1P2,C1P3,C1P4,C1P5,C1P6,C1P7,C1P8,C1P9,C1P10,C1P11,C1P12,C1PSO1,C1PSO2,C1PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO2"),C2P1,C2P2,C2P3,C2P4,C2P5,C2P6,C2P7,C2P8,C2P9,C2P10,C2P11,C2P12,C2PSO1,C2PSO2,C3PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO3"),C3P1,C3P2,C3P3,C3P4,C3P5,C3P6,C3P7,C3P8,C3P9,C3P10,C3P11,C3P12,C3PSO1,C3PSO2,C3PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO4"),C4P1,C4P2,C4P3,C4P4,C4P5,C4P6,C4P7,C4P8,C4P9,C4P10,C4P11,C4P12,C4PSO1,C4PSO2,C4PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO5"),C5P1,C5P2,C5P3,C5P4,C5P5,C5P6,C5P7,C5P8,C5P9,C5P10,C5P11,C5P12,C5PSO1,C5PSO2,C5PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO6"),C6P1,C6P2,C6P3,C6P4,C6P5,C6P6,C6P7,C6P8,C6P9,C6P10,C6P11,C6P12,C6PSO1,C6PSO2,C6PSO3))
            
            data_table.add_hline()
            
            filename = f"{subject_code}{subject_name}"
            savepath = f"syllabus/{subject_code}{subject_name}"

        filedata = {
            "filename" : filename,
            "un_name" : un_name,
            "faculty_name" : faculty_name,
            "programme" : programme,
            "branch" : branch,
            "semester" : semester,
            "version" : version,
            "effective_academic_year" : effective_academic_year,
            "effective_for_batch" : effective_for_batch,
            "subject_code" : subject_code,
            "subject_name" : subject_name,
            "lecture_credits" : lc,
            "tutorial_credits" : tuc,
            "practical_credits" : pc,
            "twc" : twc,
            "total_credits" : totalc,
            "lecture_hours" : lh,
            "tutorial_hours" : tuh,
            "practical_hours" : ph,
            "twh" : twh,
            "total_hours" : totalh,
            "ce_theory" : cet,
            "see_theory" : seet,
            "total_theory" : totalt,
            "total_theory_hours" : total_hrs,
            "ce_prctical" : cep,
            "see_practical" : seep,
            "total_practical" : totalp,
            "pre_requsites" : pre_requsites,
            
            "CO1" : CO1,"CO2" : CO2,"CO3" : CO3,"CO4" : CO4,"CO5" : CO5,"CO6" : CO6,

            "C1P1" : C1P1,"C1P2" : C1P2,"C1P3" : C1P3,"C1P4" : C1P4,"C1P5" : C1P5,"C1P6" : C1P6,"C1P7" : C1P7,"C1P8" : C1P8,
            "C1P9" : C1P9,"C1P10" : C1P10,"C1P11" : C1P11,"C1P12" : C1P12,"C1PSO1" : C1PSO1,"C1PSO2" : C1PSO2,"C1PSO3" : C1PSO3, 
            
            "C2P1" : C2P1,"C2P2" : C2P2,"C2P3" : C2P3,"C2P4" : C2P4,"C2P5" : C2P5,"C2P6" : C2P6,"C2P7" : C2P7,"C2P8" :C2P8,
            "C2P9" : C2P9,"C2P10" : C2P10,"C2P11" : C2P11,"C2P12" : C2P12,"C2PSO1" : C2PSO1,"C2PSO2" : C2PSO2,"C2PSO3" : C2PSO3,
            
            "C3P1" : C3P1,"C3P2" : C3P2,"C3P3" : C3P3,"C3P4" : C3P4,"C3P5" : C3P5,"C3P6" : C3P6,"C3P7" : C3P7,"C3P8" : C3P8,
            "C3P9" : C3P9,"C3P10" : C3P10,"C3P11" : C3P11,"C3P12" : C3P12,"C3PSO1" : C3PSO1,"C3PSO2" : C3PSO2,"C3PSO3" : C3PSO3,

            "C4P1" : C4P1,"C4P2" : C4P2,"C4P3" : C4P3,"C4P4" : C4P4,"C4P5" : C4P5,"C4P6" : C4P6,"C4P7" : C4P7,"C4P8" : C4P8,
            "C4P9" : C4P9,"C4P10" : C4P10,"C4P11" : C4P11,"C4P12" : C4P12,"C4PSO1" : C4PSO1,"C4PSO2" : C4PSO2,"C4PSO3" : C4PSO3,
            
            "C5P1" : C5P1,"C5P2" : C5P2,"C5P3" : C5P3,"C5P4" : C5P4,"C5P5" : C5P5,"C5P6" : C5P6,"C5P7" : C5P7, "C5P8" : C5P8, 
            "C5P9" : C5P9,"C5P10" : C5P10,"C5P11" : C5P11,"C5P12" : C5P12,"C5PSO1" : C5PSO1,"C5PSO2" : C5PSO2,"C5PSO3" : C5PSO3,
            
            "C6P1" : C6P1,"C6P2" : C6P2,"C6P3" : C6P3,"C6P4" : C6P4,"C6P5" : C6P5,"C6P6" : C6P6,"C6P7" : C6P7,"C6P8" : C6P8, 
            "C6P9" : C6P9,"C6P10" : C6P10,"C6P11" : C6P11,"C6P12" : C6P12,"C6PSO1" : C6PSO1,"C6PSO2" : C6PSO2,"C6PSO3" : C6PSO3,
            
            "num_of_obj" : num_of_obj,
            "num_of_unit" : num_of_unit,
            "num_of_text" : num_of_text,
            "num_of_mooc" : num_of_mooc,
            "num_of_prac" : num_of_prac,
            "num_of_ref" : num_of_ref
        }
        for i in range(0,num_of_obj):
            val = objectives[i]
            filedata[f'objective{i}'] = val
        for i in range(0,num_of_prac):
            filedata[f'practical{i}'] = practicals[i]
        for i in range(0,num_of_text):
            filedata[f'textbook{i}'] = textbooks[i]
        for i in range(0,num_of_ref):
            filedata[f'referencebooks{i}'] = referencebooks[i]
        for i in range(0,num_of_mooc):
            filedata[f'mooc{i}'] = Moocs[i]
        for i in range(0,num_of_unit):
            filedata[f'unit{i}'] = units[i]
        for i in range(0,num_of_unit):
            filedata[f'hour{i}'] = hours[i]

        fname = {
            "name":filename,
            "branch":branch
        }
        client = pymongo.MongoClient('localhost',27017)
        dbname = client['capstone']
        
        filename_collection = dbname['filename']
        filename_collection.insert_one(fname)

        filedata_collection = dbname['filecontent']
        filedata_collection.insert_one(filedata)

        try:
            doc.generate_pdf(filepath=savepath,clean=True, clean_tex=True,silent=True)
        except :
            os.remove(os.path.join("syllabus/",f"{filename}.aux"))
            os.remove(os.path.join("syllabus/",f"{filename}.log"))
            os.remove(os.path.join("syllabus/",f"{filename}.fdb_latexmk"))
            os.remove(os.path.join("syllabus/",f"{filename}.fls"))
            os.remove(os.path.join("syllabus/",f"{filename}.tex"))
            return render(request,"course/home.html")    
    return render(request,"course/home.html")

def save_edit(request):
    if request.method == "POST":
        original_filename = request.POST['filename']
        un_name = request.POST['un_name']
        faculty_name = request.POST['faculty_name']
        programme = request.POST['programme']
        branch = request.POST['branch']
        semester = request.POST['semester']
        version = request.POST['version']
        effective_academic_year = request.POST['effAY']
        effective_for_batch = request.POST['effBA']
        subject_code = request.POST['subcode']
        subject_name = request.POST['subname']
        #credits
        lc = request.POST['lc']
        tuc = request.POST['tuc']
        pc = request.POST['pc']
        twc = request.POST['twc']
        totalc = request.POST['totalc']
        #hours
        lh = request.POST['lh']
        tuh = request.POST['tuh']
        ph = request.POST['ph']
        twh = request.POST['twh']
        totalh = request.POST['totalh']
        #theory
        cet = request.POST['cet']
        seet = request.POST['seet']
        totalt = request.POST['totalt']
        #practical
        cep = request.POST['cep']
        seep = request.POST['seep']
        totalp = request.POST['totalp']

        pre_requsites = request.POST['prereq']
        
        #Get all the objectives and add to list
        objectives = []
        num_of_obj = int(request.POST['num_of_obj'])
        for i in range (0,num_of_obj):
            objective = request.POST[f'objective{i}']
            objectives.append(objective)

        #Get units and hrs
        total_hrs = 0
        units = []
        hours = []
        num_of_unit = int(request.POST["num_of_unit"])
        for i in range (0,num_of_unit):
            content = request.POST[f'content{i}']
            hrs = request.POST[f'hrs{i}']
            total_hrs = total_hrs+int(hrs)
            units.append(content)
            hours.append(hrs)

        #Get all practicals and add them to list
        practicals = []
        num_of_prac = int(request.POST['num_of_prac'])
        for i in range (0,num_of_prac):
            practical = request.POST[f'practical{i}']
            practicals.append(practical)

        #Get all textbooks and add them to list
        textbooks = []
        num_of_text = int(request.POST["num_of_text"])
        for i in range(0,num_of_text):
            textbook = request.POST[f'textbook{i}']
            textbooks.append(textbook)

        #Get all referencebooks and add them to list    
        referencebooks = []
        num_of_ref = int(request.POST["num_of_ref"])
        for i in range(0,num_of_ref):
            ref_book = request.POST[f'referencebook{i}']
            referencebooks.append(ref_book)

        #Get all ICT/mooc and add them to list
        Moocs = []
        num_of_mooc = int(request.POST["num_of_mooc"])
        for i in range(0,num_of_mooc):
            mooc = request.POST[f'mooc{i}']
            Moocs.append(mooc)

        #Course Outcomes
        CO1 = request.POST['CO1']
        CO2 = request.POST['CO2']
        CO3 = request.POST['CO3']
        CO4 = request.POST['CO4']
        CO5 = request.POST['CO5']
        CO6 = request.POST['CO6']

        #Course outcomes Mapping

        C1P1 = request.POST['C1P1']
        C1P2 = request.POST['C1P2']
        C1P3 = request.POST['C1P3']
        C1P4 = request.POST['C1P4']
        C1P5 = request.POST['C1P5']
        C1P6 = request.POST['C1P6']
        C1P7 = request.POST['C1P7']
        C1P8 = request.POST['C1P8']
        C1P9 = request.POST['C1P9']
        C1P10 = request.POST['C1P10']
        C1P11 = request.POST['C1P11']
        C1P12 = request.POST['C1P12']
        C1PSO1 = request.POST['C1PSO1']
        C1PSO2 = request.POST['C1PSO2']
        C1PSO3 = request.POST['C1PSO3']

        C2P1 = request.POST['C2P1']
        C2P2 = request.POST['C2P2']
        C2P3 = request.POST['C2P3']
        C2P4 = request.POST['C2P4']
        C2P5 = request.POST['C2P5']
        C2P6 = request.POST['C2P6']
        C2P7 = request.POST['C2P7']
        C2P8 = request.POST['C2P8']
        C2P9 = request.POST['C2P9']
        C2P10 = request.POST['C2P10']
        C2P11 = request.POST['C2P11']
        C2P12 = request.POST['C2P12']
        C2PSO1 = request.POST['C2PSO1']
        C2PSO2 = request.POST['C2PSO2']
        C2PSO3 = request.POST['C2PSO3']

        C3P1 = request.POST['C3P1']
        C3P2 = request.POST['C3P2']
        C3P3 = request.POST['C3P3']
        C3P4 = request.POST['C3P4']
        C3P5 = request.POST['C3P5']
        C3P6 = request.POST['C3P6']
        C3P7 = request.POST['C3P7']
        C3P8 = request.POST['C3P8']
        C3P9 = request.POST['C3P9']
        C3P10 = request.POST['C3P10']
        C3P11 = request.POST['C3P11']
        C3P12 = request.POST['C3P12']
        C3PSO1 = request.POST['C3PSO1']
        C3PSO2 = request.POST['C3PSO2']
        C3PSO3 = request.POST['C3PSO3']

        C4P1 = request.POST['C4P1']
        C4P2 = request.POST['C4P2']
        C4P3 = request.POST['C4P3']
        C4P4 = request.POST['C4P4']
        C4P5 = request.POST['C4P5']
        C4P6 = request.POST['C4P6']
        C4P7 = request.POST['C4P7']
        C4P8 = request.POST['C4P8']
        C4P9 = request.POST['C4P9']
        C4P10 = request.POST['C4P10']
        C4P11 = request.POST['C4P11']
        C4P12 = request.POST['C4P12']
        C4PSO1 = request.POST['C4PSO1']
        C4PSO2 = request.POST['C4PSO2']
        C4PSO3 = request.POST['C4PSO3']

        C5P1 = request.POST['C5P1']
        C5P2 = request.POST['C5P2']
        C5P3 = request.POST['C5P3']
        C5P4 = request.POST['C5P4']
        C5P5 = request.POST['C5P5']
        C5P6 = request.POST['C5P6']
        C5P7 = request.POST['C5P7']
        C5P8 = request.POST['C5P8']
        C5P9 = request.POST['C5P9']
        C5P10 = request.POST['C5P10']
        C5P11 = request.POST['C5P11']
        C5P12 = request.POST['C5P12']
        C5PSO1 = request.POST['C5PSO1']
        C5PSO2 = request.POST['C5PSO2']
        C5PSO3 = request.POST['C5PSO3']

        C6P1 = request.POST['C6P1']
        C6P2 = request.POST['C6P2']
        C6P3 = request.POST['C6P3']
        C6P4 = request.POST['C6P4']
        C6P5 = request.POST['C6P5']
        C6P6 = request.POST['C6P6']
        C6P7 = request.POST['C6P7']
        C6P8 = request.POST['C6P8']
        C6P9 = request.POST['C6P9']
        C6P10 = request.POST['C6P10']
        C6P11 = request.POST['C6P11']
        C6P12 = request.POST['C6P12']
        C6PSO1 = request.POST['C6PSO1']
        C6PSO2 = request.POST['C6PSO2']
        C6PSO3 = request.POST['C6PSO3']

        #Generate the PDF with all the data
        geometry_options = {"top":"0.96cm","right":"2.54cm","bottom":"1.93cm","left":"1.54cm"}
        doc = Document(document_options=["a4paper"],documentclass='article',geometry_options=geometry_options)
        doc.append(NoEscape(r'''\setlength{\tabcolsep}{3.5pt}
                    \centering
                '''))
        doc.packages.append(Package('longtable'))
        doc.packages.append(Package('multirow'))
        doc.packages.append(Package('enumitem'))
        doc.packages.append(Package('xcolor'))
        doc.packages.append(Package('colortbl'))

        doc.append(NoEscape(r'''\setlength{\tabcolsep}{3.5pt}
                    \centering
                '''))

        with doc.create(LongTable("|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")) as data_table:
            data_table.add_hline()
            data_table.add_row((MultiColumn(16, align='|c|',data= NoEscape(r'\LARGE{')+bold(un_name)+NoEscape(r'}')),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16, align='|c|',data= NoEscape(r'\LARGE{')+bold(faculty_name)+NoEscape(r'}')),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align='|l|',color='black!30',data="Programme"),MultiColumn(5,align='l|',data=programme),
                                MultiColumn(2,align='l|',color="black!30",data="Branch/Spec."),MultiColumn(6,align='l|',data=branch)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align='|l|',color="black!30",data="Semester"),MultiColumn(5,align='l|',data=semester),
                                MultiColumn(2,align='l|',color="black!30",data="Version"),MultiColumn(6,align="l|",data=version)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(5,align="|l|",color="black!30",data="Effective Academic Year"),MultiColumn(3,align="l|",data=effective_academic_year),
                                MultiColumn(5,align="l|",color="black!30",data="Effective for Branch admitted in"),MultiColumn(3,align="l|",data=effective_for_batch)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(3,align="|l|",color="black!30",data="Subject Code"),MultiColumn(3,align="l|",data=subject_code),
                                MultiColumn(2,align='l|',color='black!30',data="Subject Name"),MultiColumn(8,align="l|",data=subject_name)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(8,align="|l|",color="black!30", data="Teaching Scheme"),MultiColumn(8,align="l|",color="black!30",data="Examination Scheme(marks)")))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="per week"),MultiColumn(2,align="l|",data="lecture(DT)"),MultiColumn(2,align="l|",data="Practical(LAB)"),
                                MultiColumn(2,align="l|",data="Total"),MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data="CE"),
                                MultiColumn(2,align="l|",data="SEE"),MultiColumn(2,align="l|",data="Total")),color="black!30")

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data=""),"L","TU","P","TW",MultiColumn(2,align="l|",data=""),
                                MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data=""),
                                MultiColumn(2,align="l|",data=""),MultiColumn(2,align="l|",data="")))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="Credit"),lc,tuc,pc,twc,MultiColumn(2,align="l|",data=totalc),
                                MultiColumn(2,align="l|",data="Theory"),MultiColumn(2,align="l|",data=cet),MultiColumn(2,align="l|",data=seet),MultiColumn(2,align="l|",data=totalt)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(2,align="|l|",data="Hours"),lh,tuh,ph,twh,MultiColumn(2,align="l|",data=totalh),
                                MultiColumn(2,align="l|",data="Practicals"),MultiColumn(2,align="l|",data=cep),MultiColumn(2,align="l|",data=seep),MultiColumn(2,align="l|",data=totalp)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Pre-Requsites")),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",data=pre_requsites),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Objective/Learning outcomes of course")),))

            for i in objectives:
                data_table.add_row((MultiColumn(16,align="|l|",data=bold(i)),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align = NoEscape(r"|p{15cm}|"),data=["The educational objectives of course are to educate students to attain the following:"]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|l|',color="black!30",data=bold("Theory Syllabus")),))

            data_table.add_hline()
            data_table.add_row((bold("Unit"),MultiColumn(14,align='c|',data=bold("Content")),bold("Hrs")))

            i = 1
            for j,k in zip(units,hours):
                data_table.add_hline()
                data_table.add_row((bold(i),MultiColumn(14,align=NoEscape(r"|p{14cm}|"),data=j),bold(k)))
                i+=1

            data_table.add_hline()
            data_table.add_row((MultiColumn(15,align='|r|',data="Total"),total_hrs))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|l|',color="black!30",data=bold("Practical content")),))

            for i in practicals:
                data_table.add_row((MultiColumn(16,align='|l|',data=bold(i)),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Text-Books")),))

            i = 0
            for i in range(0,len(textbooks)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=textbooks[i]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("Reference Books")),))

            i = 0
            for i in range(0,len(referencebooks)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=referencebooks[i]),))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data=bold("ICT-MOOC reference")),))

            i = 0
            for i in range(0,len(Moocs)):
                data_table.add_hline()
                data_table.add_row((i+1,MultiColumn(15,align=NoEscape(r'|p{15cm}|'),data=Moocs[i]),))


            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align="|l|",color="black!30",data="Course Outcomes:"),))

            data_table.add_hline()
            data_table.add_row((bold("COs"),MultiColumn(15,align='|l|',data=bold("Description"))))

            data_table.add_hline()
            data_table.add_row((bold("CO1"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO1)))

            data_table.add_hline()
            data_table.add_row((bold("CO2"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO2)))
            
            data_table.add_hline()
            data_table.add_row((bold("CO3"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO3)))
            
            data_table.add_hline()
            data_table.add_row((bold("CO4"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO4)))

            data_table.add_hline()
            data_table.add_row((bold("CO5"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO5)))

            data_table.add_hline()
            data_table.add_row((bold("CO6"),MultiColumn(15,align=NoEscape(r"|p{15cm}|"),data=CO6)))

            data_table.add_hline()
            data_table.add_row((MultiColumn(16,align='|c|',data=bold("Mapping of Co and PO:")),))

            data_table.add_hline()
            data_table.add_row((bold("COs"),bold("PO1"),bold("PO2"),bold("PO3"),bold("PO4"),bold("PO5"),bold("PO6"),bold("PO7"),bold("PO8"),bold("PO9"),bold("PO10"),bold("PO11"),bold("PO12"),bold("PO13"),bold("PO14"),bold("PO15")))

            data_table.add_hline()
            data_table.add_row((bold("CO1"),C1P1,C1P2,C1P3,C1P4,C1P5,C1P6,C1P7,C1P8,C1P9,C1P10,C1P11,C1P12,C1PSO1,C1PSO2,C1PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO2"),C2P1,C2P2,C2P3,C2P4,C2P5,C2P6,C2P7,C2P8,C2P9,C2P10,C2P11,C2P12,C2PSO1,C2PSO2,C3PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO3"),C3P1,C3P2,C3P3,C3P4,C3P5,C3P6,C3P7,C3P8,C3P9,C3P10,C3P11,C3P12,C3PSO1,C3PSO2,C3PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO4"),C4P1,C4P2,C4P3,C4P4,C4P5,C4P6,C4P7,C4P8,C4P9,C4P10,C4P11,C4P12,C4PSO1,C4PSO2,C4PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO5"),C5P1,C5P2,C5P3,C5P4,C5P5,C5P6,C5P7,C5P8,C5P9,C5P10,C5P11,C5P12,C5PSO1,C5PSO2,C5PSO3))

            data_table.add_hline()
            data_table.add_row((bold("CO6"),C6P1,C6P2,C6P3,C6P4,C6P5,C6P6,C6P7,C6P8,C6P9,C6P10,C6P11,C6P12,C6PSO1,C6PSO2,C6PSO3))
            
            data_table.add_hline()

            filename = f"{subject_code}{subject_name}"
            savepath = f"syllabus/{subject_code}{subject_name}"

        filedata = {
            "filename" : filename,
            "un_name" : un_name,
            "faculty_name" : faculty_name,
            "programme" : programme,
            "branch" : branch,
            "semester" : semester,
            "version" : version,
            "effective_academic_year" : effective_academic_year,
            "effective_for_batch" : effective_for_batch,
            "subject_code" : subject_code,
            "subject_name" : subject_name,
            "lecture_credits" : lc,
            "tutorial_credits" : tuc,
            "practical_credits" : pc,
            "twc" : twc,
            "total_credits" : totalc,
            "lecture_hours" : lh,
            "tutorial_hours" : tuh,
            "practical_hours" : ph,
            "twh" : twh,
            "total_hours" : totalh,
            "ce_theory" : cet,
            "see_theory" : seet,
            "total_theory" : totalt,
            "total_theory_hours" : total_hrs,
            "ce_prctical" : cep,
            "see_practical" : seep,
            "total_practical" : totalp,
            "pre_requsites" : pre_requsites,
            
            "CO1" : CO1,"CO2" : CO2,"CO3" : CO3,"CO4" : CO4,"CO5" : CO5,"CO6" : CO6,

            "C1P1" : C1P1,"C1P2" : C1P2,"C1P3" : C1P3,"C1P4" : C1P4,"C1P5" : C1P5,"C1P6" : C1P6,"C1P7" : C1P7,"C1P8" : C1P8,
            "C1P9" : C1P9,"C1P10" : C1P10,"C1P11" : C1P11,"C1P12" : C1P12,"C1PSO1" : C1PSO1,"C1PSO2" : C1PSO2,"C1PSO3" : C1PSO3, 
            
            "C2P1" : C2P1,"C2P2" : C2P2,"C2P3" : C2P3,"C2P4" : C2P4,"C2P5" : C2P5,"C2P6" : C2P6,"C2P7" : C2P7,"C2P8" :C2P8,
            "C2P9" : C2P9,"C2P10" : C2P10,"C2P11" : C2P11,"C2P12" : C2P12,"C2PSO1" : C2PSO1,"C2PSO2" : C2PSO2,"C2PSO3" : C2PSO3,
            
            "C3P1" : C3P1,"C3P2" : C3P2,"C3P3" : C3P3,"C3P4" : C3P4,"C3P5" : C3P5,"C3P6" : C3P6,"C3P7" : C3P7,"C3P8" : C3P8,
            "C3P9" : C3P9,"C3P10" : C3P10,"C3P11" : C3P11,"C3P12" : C3P12,"C3PSO1" : C3PSO1,"C3PSO2" : C3PSO2,"C3PSO3" : C3PSO3,

            "C4P1" : C4P1,"C4P2" : C4P2,"C4P3" : C4P3,"C4P4" : C4P4,"C4P5" : C4P5,"C4P6" : C4P6,"C4P7" : C4P7,"C4P8" : C4P8,
            "C4P9" : C4P9,"C4P10" : C4P10,"C4P11" : C4P11,"C4P12" : C4P12,"C4PSO1" : C4PSO1,"C4PSO2" : C4PSO2,"C4PSO3" : C4PSO3,
            
            "C5P1" : C5P1,"C5P2" : C5P2,"C5P3" : C5P3,"C5P4" : C5P4,"C5P5" : C5P5,"C5P6" : C5P6,"C5P7" : C5P7, "C5P8" : C5P8, 
            "C5P9" : C5P9,"C5P10" : C5P10,"C5P11" : C5P11,"C5P12" : C5P12,"C5PSO1" : C5PSO1,"C5PSO2" : C5PSO2,"C5PSO3" : C5PSO3,
            
            "C6P1" : C6P1,"C6P2" : C6P2,"C6P3" : C6P3,"C6P4" : C6P4,"C6P5" : C6P5,"C6P6" : C6P6,"C6P7" : C6P7,"C6P8" : C6P8, 
            "C6P9" : C6P9,"C6P10" : C6P10,"C6P11" : C6P11,"C6P12" : C6P12,"C6PSO1" : C6PSO1,"C6PSO2" : C6PSO2,"C6PSO3" : C6PSO3,

            "num_of_obj" : num_of_obj,
            "num_of_unit" : num_of_unit,
            "num_of_text" : num_of_text,
            "num_of_mooc" : num_of_mooc,
            "num_of_prac" : num_of_prac,
            "num_of_ref" : num_of_ref
        }
        for i in range(0,num_of_obj):
            val = objectives[i]
            filedata[f'objective{i}'] = val
        for i in range(0,num_of_prac):
            filedata[f'practical{i}'] = practicals[i]
        for i in range(0,num_of_text):
            filedata[f'textbook{i}'] = textbooks[i]
        for i in range(0,num_of_ref):
            filedata[f'referencebooks{i}'] = referencebooks[i]
        for i in range(0,num_of_mooc):
            filedata[f'mooc{i}'] = Moocs[i]
        for i in range(0,num_of_unit):
            filedata[f'unit{i}'] = units[i]
        for i in range(0,num_of_unit):
            filedata[f'hour{i}'] = hours[i]
        

        client = pymongo.MongoClient('localhost',27017)
        dbname = client['capstone']
        filedata_collection = dbname['filecontent']
        filedata_collection.find_one_and_replace({'filename':filename},filedata)
        try:
            doc.generate_pdf(filepath=savepath,clean=True, clean_tex=True,silent=True)
        except :
            os.remove(os.path.join("syllabus/",f"{original_filename}.aux"))
            os.remove(os.path.join("syllabus/",f"{original_filename}.log"))
            os.remove(os.path.join("syllabus/",f"{original_filename}.fdb_latexmk"))
            os.remove(os.path.join("syllabus/",f"{original_filename}.fls"))
            os.remove(os.path.join("syllabus/",f"{original_filename}.tex"))
            return render(request,"course/home.html")    
    return render(request,"course/home.html")

def delete(request,fname):
    client = pymongo.MongoClient()
    dbname = client['capstone']
    filename_collection = dbname['filename']
    filename_collection.delete_one({"name":fname})

    filedata_collection = dbname['filecontent']
    filedata_collection.delete_one({'filename':fname})
    
    pdfs = filename_collection.find({})
    os.remove(os.path.join("syllabus/",f"{fname}.pdf"))
    return render(request,"course\downloads.html",
        {
            'pdfs' : pdfs
        })

