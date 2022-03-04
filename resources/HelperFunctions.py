def CreateTrainTest(data_dir, test_ratio = 0.2):
    #create the class list
    class_list = []
    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        if len(dirnames)!=0:
            class_list = dirnames
            
    #create train and test folders in data_dir
    try:
        for cls in class_list:
            os.makedirs(data_dir +'train/' + cls)
            os.makedirs(data_dir +'test/' + cls)
    except OSError:
        pass
    
    for i in class_list:
        source = data_dir + '/' + i

        #get all filenames in class-i
        allFileNames = os.listdir(source)
        np.random.shuffle(allFileNames)

        #make the split of filanames
        
        train_FileNames, test_FileNames = np.split(np.array(allFileNames),
                                                          [int(len(allFileNames)* (1 - test_ratio))])
        #path-list for train and testing filenames
        train_FileNames = [source+'/'+ name for name in train_FileNames.tolist()]
        test_FileNames = [source+'/' + name for name in test_FileNames.tolist()]

        #copy the files in /train and /test directories 
        for name in train_FileNames:
            shutil.copy(name, data_dir +'/train/' + i)
        for name in test_FileNames:
            shutil.copy(name, data_dir +'/test/' + i)
    
    print('train-test split done!')
    
def CreateSubset(data_dir,N):
    # N: number of files to left in each class
    class_paths = []            # [ [zero-paths],[one-paths], ..[nine-paths] ]
    i = 0
    for (dirpaths, dirnames, filenames) in os.walk(data_dir):
        temp = []
        if len(dirnames)==0:
            for files in filenames:
                temp.append(os.path.join(dirpaths,files))
            class_paths.append(temp)
    
    for i in range(len(class_paths)):
        folder_name = class_paths[i][0].split('/')[-2]
        number_of_files = len(class_paths[i])
        number_of_removes = number_of_files - N
        if number_of_removes <= 0:
            print(f'no removing, dont have {N} files in my folder ')
            break
        else:
            print(f'Removing {number_of_removes}/{number_of_files} files  from {folder_name}')
        for j in range(number_of_removes):
            os.remove(class_paths[i][j])
    
    print('subset created')

#CreateSubset(train_dir,50)    
#CreateSubset(test_dir,10)

def Convert2GrayScale(source_dir,target_dir):
    class_list = []
    #[[TrainClas1-paths],[TrainClas2-paths], ..[TestClas1-paths], ..]
    class_paths = [] 
    
    for (dirpath, dirnames, filenames) in os.walk(source_dir):
        if len(dirnames)!=0:
            class_list = dirnames
            
    #create train and test folders in target_dir
    try:
        for cls in class_list:
            os.makedirs(target_dir +'train/' + cls)
            os.makedirs(target_dir +'test/' + cls)

    except OSError:
        pass
    
    for (dirpaths, dirnames, filenames) in os.walk(source_dir):
        temp = []
        if len(dirnames)==0:
            for files in filenames:
                temp.append(os.path.join(dirpaths,files))
            class_paths.append(temp)

    for i in range(len(class_paths)):
            for j in range(len(class_paths[i])):
                img = Image.open(class_paths[i][j]).convert('L')
                img  = img.resize((80,80),Image.NEAREST)
                # target dest has the same structure, thus dst exactly has the same tree
                dst = class_paths[i][j].replace(source_dir,target_dir).replace('.jpg','.png')
                img.save(dst)

#grab from data_dir and resize-save to save_dir
def ResizeSave(data_dir,save_dir,dim = (224,224),RGB = True):
    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        new_paths = dirpath.replace(data_dir,save_dir)    
        if not os.path.exists(new_paths):
            os.umask(0)
            os.makedirs(new_paths, mode=0o777)
        for names in filenames:
            if RGB:
                img = Image.open(os.path.join(dirpath,names)).convert("RGB")

            else:
                img = Image.open(os.path.join(dirpath,names)).convert("L")
            img  = img.resize(dim,Image.NEAREST)
            img = img.save(os.path.join(new_paths,names))
    
    print('resizing done!')
