from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import UploadForm
import pandas as pd
import openpyxl
from .models import person
from .resources import personResources
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
import os


# Create your views here.

def uploadfile(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = pd.read_excel(request.FILES['Excel_file'])
            # write any excel modification code here 

            #store in session
            request.session['df'] = excel_file.to_dict(orient='records')
            return redirect('display_data')
            # return render (request, 'display_data.html', {'df': excel_file})
    else:
        form = UploadForm()
    return render(request, 'uploadfile.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def display_data(request):
    excel_file_records = request.session.pop('df', [])
    excel_file = pd.DataFrame(excel_file_records)

    return render (request, 'display_data.html', {'df': excel_file})


def simple_upload(request):
    if request.method == 'POST':
        person_resource = personResources()
        dataset = Dataset()
        new_person = request.FILES['myfile']

        imported_data = dataset.load(new_person.read(),format='xlsx')
        for data in imported_data:
            value = person(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
    return render(request,'data_upload.html')

def export(request):
    person_resource = personResources()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="person.xls"'
    return response
    


###############################################################################################################

from django.core.files.storage import FileSystemStorage, default_storage
from .forms import ExcelUploadForm
from .models import ExcelData, File


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            df_list = []

            for uploaded_file in files:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                df = pd.read_excel(uploaded_file)
                df_list.append(df)

                ExcelData.objects.create(file=filename)

            # Merge the dataframes
            final_df = pd.concat(df_list, ignore_index=True)

            # Save the final_df to a new Excel file or process it as needed
            output_file_path = 'path_to_final_output_file.xlsx'
            final_df.to_excel(output_file_path, index=False) 

            success_message = f'{len(files)} files uploaded successfully'

            return redirect('upload_excel')
            # return render(request, 'upload_excel.html', {'form': form, 'success_message': success_message})
        
            # return render(request, 'merge_excel.html', {'output_file_path': output_file_path})

    else:
        form = ExcelUploadForm()

    data = ExcelData.objects.all()
    return render(request, 'upload_excel.html', {'form': form, 'data': data})


def merge_excel(request):
       # Logic to merge Excel files and create the final Excel file
       # You can use pandas library for handling Excel files

       # For example:
    data = ExcelData.objects.all()
    df_list = [pd.read_excel(data_obj.file.path) for data_obj in data]
    final_df = pd.concat(df_list, ignore_index=True)

       # Save the final_df to a new Excel file or process it as needed
    final_df.to_excel(r"C:\Users\medas\OneDrive\Desktop\Output.xlsx", index=False)

    return render(request, 'merge_excel.html')


def delete_excel(request, file_id):
       # Retrieve the ExcelData object based on the file_id
    excel_data = ExcelData.objects.get(pk=file_id)

       # Delete the associated file from the storage
    file_path = excel_data.file.path
    os.remove(file_path)

       # Delete the ExcelData object from the database
    excel_data.delete()

    return redirect('upload_excel')

def file_list(request):
    files = File.objects.filter(deleted=False)
    context = {'files': files}
    return render(request, 'your_template.html', context)


###################################################################################################################################################

from .forms import ExcelIndividualForm, ExcelDeleteForm
from .models import ExcelIndividual

def upload_separate_excel(request):
    if request.method == 'POST':
        form = ExcelIndividualForm(request.POST, request.FILES)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            excel_file = form.cleaned_data['excel_file']
            # files = request.FILES.getlist('excel_file')
            # df_list = []

            # for uploaded_file in files:
            #     fs = FileSystemStorage()
            #     filename = fs.save(uploaded_file.name, uploaded_file)
                
            #     df = pd.read_excel(uploaded_file)
            #     df_list.append(df)

            #     ExcelData.objects.create(name=user_name, file=filename)

            # Merge the dataframes
            # final_df = pd.concat(df_list, ignore_index=True)

            # Save the final_df to a new Excel file or process it as needed
            # output_file_path = 'path_to_final_output_file.xlsx'
            # final_df.to_excel(output_file_path, index=False)
            # Book4.to_excel(output_file_path, index=False)

            # return redirect('upload_separate_success')
            # return render(request, 'merge_excel.html', {'output_file_path': output_file_path})
            # Rename the file with the user_name
           # Rename the file with the user_name
            file_name, file_extension = os.path.splitext(excel_file.name)
            new_file_name = f"{user_name}{file_extension}"

            # Save the uploaded file to the model
            instance = ExcelIndividual(user_name=user_name, excel_file=new_file_name)
            instance.excel_file.save(new_file_name, excel_file, save=True)

            # Read the Excel file and save data to the database
            df = pd.read_excel(excel_file)
            # YourModel.objects.bulk_create([YourModel(**row) for row in df.to_dict(orient='records')])

            return redirect('upload_separate_excel')
    else:
        form = ExcelIndividualForm()

    files = ExcelIndividual.objects.all()  # Query all uploaded files
    return render(request, 'upload_separate_excel.html', {'form': form, 'files': files})



    # else:
    #     form = ExcelIndividualForm()

    # data = ExcelIndividual.objects.all()
    # delete_form = ExcelDeleteForm()
    # return render(request, 'upload_separate_excel.html', {'form': form, 'data': data, 'delete_form': delete_form})


# def merge_excel(request):
#        # Logic to merge Excel files and create the final Excel file
#        # You can use pandas library for handling Excel files

#        # For example:
#     data = ExcelIndividual.objects.all()
#     df_list = [pd.read_excel(data_obj.file.path) for data_obj in data]
#     final_df = pd.concat(df_list, ignore_index=True)

#        # Save the final_df to a new Excel file or process it as needed
#     final_df.to_excel(r"C:\Users\medas\OneDrive\Desktop\Output.xlsx", index=False)

#     return render(request, 'merge_excel.html')


def delete_separate_excel(request):

    if request.method == 'POST':
        delete_form = ExcelDeleteForm(request.POST)
        if delete_form.is_valid():
            file_id = delete_form.cleared_data['excel_file_id']
       # Retrieve the ExcelData object based on the file_id
    
            excel_data = ExcelIndividual.objects.get(pk=file_id)

       # Delete the associated file from the storage
            file_path = excel_data.file.path
            fs = FileSystemStorage()
            fs.delete(file_path)


       # Delete the ExcelData object from the database
            excel_data.delete()
            return redirect('upload_separate_excel')

    return redirect('upload_separate_excel')

def upload_separate_success(request):
    return render(request, 'upload_separate_success.html')



####################################################################################################################################

from .forms import UserDataForm
from .models import UserData

def process_excel(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.save(commit=False)

               # Rename the file with the username
            user_data.excel_file.name = f"{user_data.username}.xlsx"

            user_data.save()

            return redirect('file_list')
    else:
        form = UserDataForm()
    return render(request, 'upload_form.html', {'form': form})

def file_list(request):
    files = UserData.objects.all()
    return render(request, 'file_list.html', {'files': files})

def delete_file(request, file_id):
    file = get_object_or_404(UserData, pk=file_id)
    file_path = file.excel_file.path
    file.excel_file.delete()
    file.delete()
    return redirect('file_list')



def merge_data(request):
       # Get all UserData instances
    all_user_data = UserData.objects.all()

       # Check if there are at least two files to merge
    if len(all_user_data) < 2:
        return render(request, 'merge_error.html', {'error_message': 'Insufficient files for merging.'})

       # Read and concatenate data from all files
    dfs = [pd.read_excel(user_data.excel_file.path) for user_data in all_user_data]
    merged_df = pd.concat(dfs, ignore_index=True)

       # Example: Save the merged DataFrame to a new file
    merged_file_name = 'merged_data.xlsx'
    merged_file_path = f'media/{merged_file_name}'
    merged_df.to_excel(merged_file_path, index=False)

    print(merged_file_path)

       # Create a UserData instance for the merged file
    # merged_user_data = UserData.objects.create(username='merged_user', excel_file='merged_data.xlsx')

    return render(request, 'merge_success.html', {'merged_file_path': merged_file_path, 'merged_df': merged_df})


# @require_http_methods(["POST"])
def delete_merged_file(request, merged_file_path):
       # Get the UserData instance for the merged file
    # merged_user_data = get_object_or_404(UserData, pk=merged_file_id)

       # Delete the merged file from storage
    # merged_file_path.delete()

       # Delete the UserData instance for the merged file
    # merged_user_data.delete()

    # return redirect('process_excel')
    try:
    #     # Construct the full path to the file within your app's media directory
        full_path = merged_file_path
        if os.path.exists(full_path):
            os.remove(full_path)

    #     # Check if the file exists before attempting to delete
    #     if default_storage.exists(merged_file_path):
    #         # Delete the file
    #         default_storage.delete(merged_file_path)

    #         # Return a success message
            return HttpResponse(f"File at {merged_file_path} deleted successfully.")
        else:
            return HttpResponse(f"File at {merged_file_path} not found.")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")

    # full_path = default_storage.path(merged_file_path)
    #         # Delete the file
    # default_storage.delete(merged_file_path)
    # return redirect('process_excel')



def merge_error(request):
    return render(request, 'merge_error.html')