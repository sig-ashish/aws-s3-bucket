from flask import render_template, url_for, flash, redirect, request
from main import app, db
from main.forms import RegistrationForm, LoginForm, RedirectToFolder, RenameFileForm, CreateFolderForm
from main.models import User 
from main.boto_s3 import create_folder, delete_folder, get_bucket_list,\
                            get_bucket_details, \
                            get_folder_details,\
                            upload_file ,\
                                delete_file, rename_file,\
                                    copy_to_bucket



@app.route("/")
@app.route("/home", methods=['GET', 'POST'] )
def home():
    form = RedirectToFolder()
    buckets_list = get_bucket_list() 
    return render_template('buckets.html',buckets_list=buckets_list,form =form)


@app.route("/buckets" , methods=['GET', 'POST'])
def buckets():
    form = RedirectToFolder()
    buckets_list = get_bucket_list() 
    return render_template('buckets.html',buckets_list=buckets_list,form =form)


@app.route("/folders/<bucket_name>" ,methods =['POST','GET'])
def folders(bucket_name):
    folders_list , bucket_name = get_bucket_details(bucket_name)
    return render_template('folders.html',folders_list = folders_list, bucket_name = bucket_name)



@app.route("/files/<bucket_name>/<folder_name>/")
def files(bucket_name,folder_name):
    form = RenameFileForm()
    buckets = get_bucket_list()
    folders_list , bucket_name_ = get_bucket_details(bucket_name)
    buckets_list = [ x['Name'] for x in buckets['Buckets']]
    files_list , file_names = get_folder_details(bucket_name,folder_name)
    return render_template("files.html",files_list=files_list,form =form,buckets_list =buckets_list, file_names=file_names) 

@app.route('/upload', methods=['POST'])
def upload():            
    file = request.files['file_name']
    filename = request.files['file_name'].filename 
    bucket = str(request.form['bucket_name'])
    args = {'ACL':'public-read'}
    folder = request.form['folder_name']
    key = folder+"/"+ filename
    upload_file(file,bucket,key,args)
    flash('File uploaded successfully')
    return redirect(url_for('files', bucket_name = bucket,folder_name = folder))

@app.route('/delete', methods=['POST'])
def delete():            
    file = request.form['file_name']
    folder_name = request.form['folder_name']
    bucket_name = str(request.form['bucket_name'])
    delete_file(bucket_name,file)
    return redirect(url_for('files', bucket_name= bucket_name,folder_name = folder_name))

@app.route('/rename', methods=['POST'])
def rename():            
    old_name = request.form['old_name']
    folder_name = request.form['folder_name']
    new_name = folder_name +"/"+ request.form['new_name']
    
    bucket_name = str(request.form['bucket_name'])
    rename_file(bucket_name,folder_name,new_name,old_name)
    return redirect(url_for('files', bucket_name= bucket_name,folder_name = folder_name))

@app.route('/copy', methods=['POST'])
def copyfile():       
    source_bucket = str(request.form['source_bucket'])
    folder_name = request.form['folder_name']
    source_key = request.form['source_key']
    other_bucket = request.form['other_bucket']
    otherkey = request.form['other_folder'] +"/" + request.form['otherkey']

    copy_to_bucket(source_bucket,source_key,other_bucket,otherkey)
    return redirect(url_for('files', bucket_name= source_bucket,folder_name = folder_name))

@app.route('/createfolder', methods=['POST'])
def createfolder():       
    bucket_name = str(request.form['bucket_name'])
    folder_name = request.form['folder_name'] + "/"
    create_folder(bucket_name,folder_name)
    return redirect(url_for('folders', bucket_name=bucket_name))

@app.route('/deletefolder', methods=['POST'])
def deletefolder():       
    bucket_name = str(request.form['bucket_name'])
    folder_name = request.form['folder_name']
    delete_folder(bucket_name,folder_name)
    return redirect(url_for('folders', bucket_name=bucket_name))

@app.route('/movefile', methods=['POST'])
def movefile():       
    source_bucket = str(request.form['source_bucket'])
    folder_name = request.form['folder_name']
    source_key = request.form['source_key']
    other_bucket = request.form['other_bucket']
    otherkey = request.form['other_folder'] +"/" + request.form['otherkey']
    copy_to_bucket(source_bucket,source_key,other_bucket,otherkey)
    delete_file(source_bucket,source_key)
    
    return redirect(url_for('files', bucket_name= source_bucket,folder_name = folder_name))
