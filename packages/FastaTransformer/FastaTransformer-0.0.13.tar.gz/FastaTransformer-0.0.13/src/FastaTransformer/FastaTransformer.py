def FastaToAlignment(input_file = 'output_endcount.fasta', output_file = 'output_aligned.fasta', musclepath = 'muscle3.8.31_i86win32.exe', gapextpenalty = -1.0, gapopenpenalty = -10.0):
    
    """
    Takes a .fasta file and uses the Muscle program via MuscleCommandLine to output an alignment file. Inputs are filepath locations, except for gapextpenalty and gapopenpenalty which are aspects of Muscle. It can be applied to an entire folder of .fasta files using :func:`GeneBankToAlignmentBank`.
    
    Documentation for .fasta files can be found at https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ and examples provided at https://en.wikipedia.org/wiki/FASTA_format#Description_line.

    Parameters
    ---
    input_file : String of a path to an input .fasta file.

    output_file : String of a path to an output .fasta file.
    
    musclepath : String of a path to the Muscle installation, a .exe file.

    gapextpenalty : Negative Float. Default value of -1.0.

    gapopenpenalty : Negative Float. Default value of -10.0.

    Returns
    ---
    An alignment .fasta file.

    Examples
    ---
    >>> input_file
    >>> .\\FastaBank\\Gene01.fasta
    >Genome01
    AAAABC
    >Genome02
    AAABC

    >>> output_file
    >>> .\\AlignmentBank\\Gene01.fasta
    >Genome01
    AAAABC
    >Genome02
    AAA-BC

    """

    from Bio.Align.Applications import MuscleCommandline
    import os
    with open(output_file, 'w') as fp:
        pass
    
    muscle_exe =  musclepath
    in_file = input_file
    out_file = output_file
    muscle_cline = MuscleCommandline(muscle_exe, input=in_file, out=out_file, gapextend = gapextpenalty, gapopen = gapopenpenalty) 
    os.system(str(muscle_cline))

def FolderPathFixer(FolderPath):
    """
    An internal function used to fix folder paths.
    
    Parameters
    ---
    A path to a folder.
    
    Returns
    ---
    The folder path, if not made, will be made. Additionally, a "\\" will be added at the end to allow more items to the end.
    """
    import os
    os.makedirs(FolderPath, exist_ok=True)
    return FolderPath + "\\"

def MakeGeneBank(input_csv, FastaBank, Seq = "Sequence", ID = "Genome", Grouping = "Gene", DropDuplicates = "Partial", DeleteStar = True):

    """
    Take an input csv with Genomes, their genes, and their sequences and split them into a series of .fasta files with the title of the gene and each entry described as a geneome. The output of this function can be fed into :func:`GeneBankToAlignmentBank`.

    Documentation for .fasta files can be found at https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ and examples provided at https://en.wikipedia.org/wiki/FASTA_format#Description_line.
    
    Parameters
    ---
    input_csv : A CSV or pd.DataFrame containing columns for a sequence, genome, and genes to be converted into Fasta files.
    
    FastaBank : String of a path to a folder to place the .fasta files in.
    >>> Example
    "Project_AD-Unique Protein Sequences in new Genomes\\FastaBank\\"
    
    Seq : A string indicating the column of the CSV used to indicate the sequence. Default "Sequence".
    
    ID : A stirng indicating the column of the CSV used to indicate the Accession, Genome, or Identifier of the Sequence. Default "Genome".
    
    Grouping : A string indicating the column of the CSV used to split the sequences into different .fasta files. Default "Gene".
    
    DropDuplicates : Indicates if Duplicate Sequences in a Grouping (Such as Gene) should be dropped. Increases computational time. Default Partial.
        All : Remove all identical Seq in a Grouping
        Partial : Remove idential entries only if ID, Seq, and Grouping are the Same
    
    DeleteStar : Indicates if values after an * should be deleted from each sequence, to only keep the portion before the sequences end. Default True.

    Returns
    ---
    Fills the selected FastaBank folder by splitting the rows of the input_csv.

    It also returns a dataframe of all duplicate genes in each genome to allow bugfixing.

    Examples
    ---
    >>> MakeGeneBank('FixSamTSV Code\\p72 Genotyping Website\\Data\\currated_ASFV_db_v02.csv','FixSamTSV Code\\p72 Genotyping Website\\Data\\FastaBank')

    """

    import pandas as pd
    if type(input_csv) == type("ABC"):
        input_df = pd.read_csv(input_csv)
    else:
        input_df = input_csv
    try:
        input_df[Grouping] = input_df[Grouping].str.replace('\*', "", regex=True)
    except:
        pass
    if DropDuplicates == "All":
        input_df = input_df.drop_duplicates([Grouping, Seq])
    if DropDuplicates == "Partial":
        input_df = input_df.drop_duplicates([Grouping, Seq, ID])

    Groups = input_df.groupby(Grouping)

    keys = Groups.groups.keys()

    FastaBank = FolderPathFixer(FastaBank)

    BugBank = pd.DataFrame(columns=[Seq, Grouping, ID])
    for name, group in Groups:
        
        try:
            if len(group[group.duplicated([ID], keep=False)]) > 0:
                print(group[group.duplicated([ID], keep=False)].drop(['Unnamed: 0'], axis=1))
                BugBank = pd.concat([BugBank,(group[group.duplicated([ID], keep=False)]).drop(['Unnamed: 0'], axis=1)])
        except:
            try:
                if len(group[group.duplicated([ID], keep=False)]) > 0:
                    BugBank = pd.concat([BugBank,group[group.duplicated([ID], keep = False)]])
                    group = group.drop_duplicates([ID], keep=False)
            except:
                print("Failed to run, likely duplicates with " + name + " , skipping")
                continue
            
        for index, row in group.iterrows():        
            outputname_fasta = FastaBank + str(name).replace('/', '-') + ".fasta"
            try:
                if DeleteStar == True:
                    row[Seq] = row[Seq].split('*', 1)[0]

                with open(outputname_fasta, "a") as f:
                        print(">" + str(row[ID]) + "\n" + str(row[Seq]).replace("[", "").replace("]", "").replace("'", ""), file = f)
            except:
                try: 
                    print("Failed to Format")
                    print(row)
                except:
                    print("Failed to Format")
                    print(name)
                continue
    return BugBank

def GeneBankToAlignmentBank(FastaBank, AlignmentBank, musclepath = 'muscle3.8.31_i86win32.exe', gapextpenalty = -1.0, gapopenpenalty = -10.0):
    
    """
    Take a folder of .fasta files seperated by gene, and create a matching folder of alignment files using the :func:`FastaToAlignment` function.

    Documentation for .fasta files can be found at https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ and examples provided at https://en.wikipedia.org/wiki/FASTA_format#Description_line.

    Parameters
    ---
    FastaBank : String of a path to a folder containing the .fasta files. A FastaBank can be created using the :func:`MakeGeneBank` function.
    >>> Example
    "Project_AD-Unique Protein Sequences in new Genomes\\FastaBank"

    AlignmentBank : String of a path to a folder to place the alignments corresponding with those in the FastaBank.
    >>> Example
    "Project_AD-Unique Protein Sequences in new Genomes\\AlignmentBank"

    musclepath : String of a path to the Muscle installation to be used in the wrapped function :func:`FastaToAlignment`.

    gapextpenalty : Negative Integer. Default value of -1.0.

    gapopenpenalty : Negative Integer. Default value of -10.0.

    Returns
    ---
    Fills the selected AlignmentBank folder with .fasta files corresponding to those in FastaBank.

    Examples
    ---
    >>> GeneBankToAlignmentBank('WebSite_LSDV\\FastaBank','WebSite_LSDV\\AlignmentBank')

    """
    FastaBank = FolderPathFixer(FastaBank)
    AlignmentBank = FolderPathFixer(AlignmentBank)
    
    import glob
    my_files = glob.glob(FastaBank + '*')
    for fasta in my_files:
        ouputfasta = fasta.replace(FastaBank, AlignmentBank)
        FastaToAlignment(fasta, ouputfasta, musclepath, gapextpenalty = gapextpenalty,gapopenpenalty = gapopenpenalty)

def InputToList(Object, Keyword = None):

    """Take a list, a pd.Series, or a pd.DataFrame with a specific keyword and return a list of unique strings in that list. Used in this package to prevent failures caused by different uplaod types. Used as a starting function in other functions to help put parameters into a correct format.
    
    Parameters
    ---
    Object : a list, pd.Series, or pd.Dataframe with Keyword set to a value other than None.

    Keyword : Used to designate the column to be used in the case that a pd.DataFrame is submitted.
    
    Returns
    ---
    A list of unique strings.
    """

    import pandas as pd
    if type(Object) is list:
            Output = list(set(Object))
    elif type(Object) is pd.Series:
        Output = list(Object.unique())
    elif type(Object) is pd.DataFrame:
        Output = list(Object[Keyword].unique())
    return Output

def HashtagCSVtoDf(CSV, infocolumn = 'AccessGene', sep = "###", columnone = 'Gene', columntwo = 'Genome'):
    """
    The purpose of this code is to upload a csv and change the designated infocolumn into a pair of columns.

    Requirements
    ---
    Pandas module, which is likely included with your python installtion.
    
    Parameters
    ---

    CSV : String of the csv file path.
    >>> Example: "Project_AD-Unique Protein Sequences in new Genomes\\InputFiles\\All Cameroon Translations.csv"
    
    infocolumn : string, default "AcessGene".
    
    sep : string object that seperates names of variables, default "###".
    
    columnone : string, default "Gene".
    
    columntwo : string, default "Genome".


    Returns
    ---
    A pd.dataframe object.

    Examples
    ---
    >>> Example Input 
    >>> df
        Sequence        AcessGene
    0   MSLWPPQKKVF...  ASFV-G (Georgia-2007)###DP60R
    1   MNIYLVWFLYI...  ASFV-G (Georgia-2007)###ASFV G ACD 01990

    >>> Example Output
    >>> df
        Sequence         Gene                Genome
    0   MSLWPPQKKVF...   DP60R               ASFV-G (Georgia-2007)
    1   MNIYLVWFLYI...   ASFV G ACD 01990    ASFV-G (Georgia-2007)

    """
    
    import pandas as pd

    df = pd.read_csv(CSV)
    sep = "###"
    df[columnone] = df[infocolumn].map(lambda x: x[x.find(sep)+len(sep):])
    df[columntwo] = df[infocolumn].map(lambda x: x[:x.find(sep)])
    df = df.drop(infocolumn, axis = 1)
    return df

def AlignmentChangeFinder(AlignmentBank, NewGenomeNames, OldGenomeNames, SpecialReference = None):
    """
    A function intended to find novel (unique) changes in genes between a set of new genomes and reference ('old') genomes using a set of .fasta files. The function returns a specially formatted dataframe.

    Documentation for .fasta files can be found at https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ and examples provided at https://en.wikipedia.org/wiki/FASTA_format#Description_line.

    Parameters
    ---
    AlignmentBank : String of the path to a folder containing .fasta files with the file named after a gene and the sequences named after the genomes. An AlignmentBank can be generated using the :func:`GeneBankToAlignmentBank` function in this package. 
    >>> Example
    "Project_AD-Unique Protein Sequences in new Genomes\\AlignmentBank"
    
    NewGenomeNames : A list of strings containing the names of genomes to be tested. Must match the genome names used in the AlignmentBank. Can also be submitted as a pd.Series (such as by using df['GenomeColumnName'] for the df that generated the Fasta\\AlignmentBanks).
    >>> Example
    ['Cameroon_2016_C1', 'Cameroon_2016_C5', 'Cameroon_2017_C-A2', 'Cameroon_2018_C02', 'Cameroon_2018_C-F3']
    
    OldGenomeNames : A list of strings containing the names of genomes to be references against. Must match the genome names used in the AlignmentBank. Can also be submitted as a pd.Series (such as by using df['GenomeColumnName'] for the df that generated the Fasta\\AlignmentBanks).
    >>> Example
    ['ASFV-G (Georgia-2007)', 'Malawi Lil-20/1 (Malawi: Chalaswa-1983)', 'L60 (Portugal-1960)', 'BA71V (Spain-1971)', 'Benin 97/1 (Benin-1997)', 'E75 (Spain-1975)', 'OURT 88/3 (Portugal-1988)', 'Warmbaths (South Africa: Warmbaths-1987)', 'Warthog (Namibia-1980)', 'Ken05/Tk1 (Kenya-2005)', 'Ken06.Bus (Kenya-2006)', 'Kenya 1950 (Kenya-1950)', 'Mkuzi 1979 (South Africa: Mkuzi Game Reserve-1979)', 'Tengani 62 (Malawi: Tengani-1962)', 'Pretorisuskop/96/4 (South Africa: Kruger National Park-1996)', 'NHV (Portugal-1968)']

    SpecialReference : If measurements are desired against a specific old/reference geneome, set this equal to the name of a string in OldGenomes. Default value is None.
    >>> Example
    'Benin 97/1 (Benin-1997)'

    Returns
    ---
    The function returns a dataframe that contains all data. This dataframe can be fed into :func:`AlignmentChangeFinderSelector` and/or :func:`AlignmentChangeFinderCleanup` to clean up and select wanted results.
    >>> df
                Gene1   Gene2
    NewGeneome1 list11  list12
    NewGeneome2 list21  list22

    Each list contains elements indicating unique differences between the 'New' Genomes and the Old/reference Genomes. Each element is a formatted string with the following parts, with each part name in parenthesis followed by its data:

    RefAA : A letter indicating the ammino acid changed from in the SpecialReference version of the gene. Only present if a SpecialReference is provided.

    RefPos : A number indicating the position in the SpecialReference version of the gene where the change took place (this number is different from AlignPos because it does not count gaps). Only present if a SpecialReference is provided. Positions begin at 1, not 0.

    Old : The Ammino Acids present in all the reference strains, by number. Each Ammino acid is followed by #, then the number of ammino acids at the Alignposition of that type, then . and the next ammino acid present.
    
    AlignPos : A number indicating the position in the Alignment version of the gene where the change took place (counting gaps). Only present if a SpecialReference is provided. Positions begin at 1, not 0.

    SelfPos : A number indicating the position in the New Genome version of the gene where the change took place (this number is different from AlignPos because it does not count gaps). Positions begin at 1, not 0.

    SelfAA : A letter indicating the ammino acid changed to in the new Genome.

    >>> Example
    ['(RefAA)V (RefPos)104 (Old)V#16.-#12.S#5 (AlignPos)105 (SelfPos)104 (SelfAA)I']

    """
    import Bio.SeqIO as SeqIO
    import pandas as pd
    import glob

    NewGenomeNames = InputToList(NewGenomeNames, 'Genomes')
    OldGenomeNames = InputToList(OldGenomeNames, 'Genomes')
    AlignmentBank = FolderPathFixer(AlignmentBank)
    
    if SpecialReference != None:
        if SpecialReference not in OldGenomeNames:
            print("SpecialReference Must be in OldGenomeNames, To Avoid Error SpecialReference set to None")

    my_files = glob.glob(AlignmentBank + '*')
    FinalFrame = pd.DataFrame(NewGenomeNames, columns=['id']).set_index('id')
    for fasta in my_files:

        #fasta = AlignmentBank+'B962L.fasta'
        gene = fasta.replace(AlignmentBank, "").replace(".fasta", "").replace(".fa", "")

        df = pd.DataFrame(columns=['id', 'sequence'])
        for Genome in SeqIO.parse(fasta,format='fasta'):
            df.loc[len(df.index)] = [Genome.description, str(Genome.seq)]

        Old_df = df[df['id'].isin(OldGenomeNames)].set_index('id')

        if SpecialReference != None:
            try:
                Spec_Seq = df[df['id'] == SpecialReference].set_index('id').iloc[0]['sequence']
            except:
                Spec_Seq = None
        else:
            Spec_Seq = None

        New_df = df[df['id'].isin(NewGenomeNames)].set_index('id')

        #Checking for a destructive bug
        if len(New_df) > len(FinalFrame):
            print(str(gene) + "likely has duplicate genes. Results ommitted to prevent crash.")
            continue

        AllSequences = []
        for sequence in list(map(''.join, zip(*Old_df['sequence']))):
            AllSequences.append('.'.join([i + "#" + str(sequence.count(i)) for i in set(sequence)]))
        
        def FindFlaw(Sequence, CompareSequences, Spec_Seq = None):
            Flaw = []
            try:
                for i in range(len(Sequence)):
                    if Sequence[i] not in CompareSequences[i]:
                        
                        if Spec_Seq == None:
                            SSinfo = ""
                        else:
                            SSinfo =  "(RefAA)"+Spec_Seq[i] + " " + "(RefPos)"+str(len(Spec_Seq[:i+1].replace("-",""))) + " "

                        Flaw.append(SSinfo + "(Old)" + CompareSequences[i]+ " " + "(AlignPos)" + str(i+1) + " " + "(SelfPos)" + str(len(Sequence[:i+1].replace("-",""))) + " " + "(SelfAA)" + Sequence[i])
                if len(Sequence) == 0:
                    return "NA"
                if len(Flaw) == 0:
                    return ""
                return Flaw
            except:
                print("Failed At FindFlaw on " + fasta)
                return "ERROR"
        
        try:
            results = pd.DataFrame()
            results[str(gene)] = New_df['sequence'].map(lambda x: FindFlaw(x, AllSequences, Spec_Seq))
            FinalFrame = pd.concat([FinalFrame,results], axis=1)
        except:
            print("Failed at Final Frame Concatonation at " + fasta)
            continue

    return FinalFrame

def AlignmentChangeFinderSelector(df, GeneList = None, DropNA = True):
    
    """
    A function that selects the specific outputs of the :func:`AlignmentChangeFinder` that are desired.

    Parameters
    ---
    df : A dataframe constructed by :func:`AlignmentChangeFinder`.

    Genelist : A list, or pd.Series object with a list of Genes to be kept. All other genes will be removed.

    DropNa : Drop all genes only containing NaN entries. Does not include Genes that are empty because there were no genes missing in the Genomes and differences were not found.

    Returns
    ---
    Returns a dataframe modified to remove values the user is not interested in.
    """

    if GeneList != None:
        GeneList = InputToList(GeneList, 'Gene')
        df = df[GeneList]
    if DropNA == True:
        df = df.dropna(how='all', axis=1)
    return df

def Rangemaker(info, FirstAA, FirstPositions):
        
        """
        A function for cleaning up a list object within a pd.DataFrame produced by :func:`AlignmentChangeFinder` into a more interpretable form. This function primarily exists for development purposes. To convert an entire pd.DataFrame, use its wrapper, :func:`AlignmentChangeFinderCleanup`.

        Parameters
        ---
        info : A list entry in a pd.DataFrame constructed by :func:`AlignmentChangeFinder`.

        FirstAA : Indicates which Ammino Acid should be shown for the result. Options include:

            'Ref' : Use the Ammino Acid indicated by (RefAA). Default option.

            'Majority' : Uses the most common Ammino Acid in the (Old) substring.

        FirstPositions : Indicates which positional marker should be shown for the result. Options include:

            'Ref' :  Use the position from the (RefPos) substring. Does not include gaps. Default option.

            'Self' : Use the data in the (SelfPos) substring. Does not include gaps.

            'Align' : Use the data in the (AlignPos) substring.

        Returns
        ---
        A cleaned up string in place of the list. The string is the chosen ammino acid, chosen position, and final ammino acid (followed by a comma and any other aread). In the case there are continous positions in the list, the elements are combined into a single entry. If either the chosen ammino acid or the final position are the same indicator, they are converted to one object (for example, AAAA173TQKY would become A173TQKY).

        >>> An example list before cleanup.
        ['(RefAA)C (RefPos)352 (Old)Y#3.C#10.-#3 (AlignPos)386 (SelfPos)334 (SelfAA)G', '(RefAA)P (RefPos)353 (Old)S#2.P#11.-#3 (AlignPos)387 (SelfPos)335 (SelfAA)R', '(RefAA)K (RefPos)356 (Old)K#8.E#3.-#5 (AlignPos)390 (SelfPos)338 (SelfAA)H', '(RefAA)C (RefPos)358 (Old)Y#1.H#1.C#9.-#5 (AlignPos)392 (SelfPos)340 (SelfAA)G', '(RefAA)S (RefPos)366 (Old)S#8.-#8 (AlignPos)400 (SelfPos)348 (SelfAA)P', '(RefAA)E (RefPos)368 (Old)E#7.-#9 (AlignPos)402 (SelfPos)350 (SelfAA)K', '(RefAA)S (RefPos)369 (Old)S#6.T#1.-#9 (AlignPos)403 (SelfPos)351 (SelfAA)P', '(RefAA)Y (RefPos)370 (Old)Y#8.-#8 (AlignPos)404 (SelfPos)352 (SelfAA)C', '(RefAA)S (RefPos)371 (Old)S#8.-#8 (AlignPos)405 (SelfPos)353 (SelfAA)P']
        >>> Changed Example
        'CP352-353GR, K356H, C358G, S366P, ESYS368-371KPCP'

        Warnings
        ---
        If there are no references in the info list, then the output ['NoReference'] will be given instead.

        """

        import pandas as pd

        if FirstAA or FirstPositions == 'Ref':
            if '(RefPos)' not in info[0]:
                return ['NoReference']

        Positions = []
        AAFirst = []
        AALast = []       
        
        for string in info:
            splitstring = string.split(" ")
            AALast.append(list(filter(lambda x: '(SelfAA)' in x, splitstring))[0].replace('(SelfAA)',""))
            if FirstPositions == 'Self':
                Positions.append(int(list(filter(lambda x: '(SelfPos)' in x, splitstring))[0].replace('(SelfPos)',"")))
            if FirstPositions == 'Ref':
                Positions.append(int(list(filter(lambda x: '(RefPos)' in x, splitstring))[0].replace('(RefPos)',"")))
            if FirstPositions == 'Align':
                Positions.append(int(list(filter(lambda x: '(AlignPos)' in x, splitstring))[0].replace('(AlignPos)',"")))
            if FirstAA == 'Ref':
                AAFirst.append(list(filter(lambda x: '(RefAA)' in x, splitstring))[0].replace('(RefAA)',""))
            if FirstAA == 'Majority':
                Old = list(filter(lambda x: '(Old)' in x, splitstring))[0].replace('(Old)',"").split('.')
                OldAA = []
                OldCount = []
                for OldEntry in Old:
                    OldAA.append(OldEntry.split('#')[0])
                    OldCount.append(int(OldEntry.split('#')[1]))
                AAFirst.append(OldAA[OldCount.index(max(OldCount))])
        
        #Identify Ranges
        from itertools import groupby
        from operator import itemgetter
        listdf = pd.DataFrame(list(zip(AAFirst, Positions, AALast)), columns=['AAFirst','Positions','AALast']).sort_values('Positions', ascending=True)    
        data = sorted(set(Positions))
        Ranges = []
        for k, g in groupby(enumerate(data), lambda ix : ix[0] - ix[1]):
            Rangedf = listdf.loc[listdf['Positions'].isin(list(map(itemgetter(1), g)))]

            AAFirstRange = ''.join(list(Rangedf['AAFirst']))
            if len(set(AAFirstRange)) == 1:
                AAFirstRange = ''.join(set(AAFirstRange))
            AALastRange = ''.join(list(Rangedf['AALast']))
            if len(set(AALastRange)) == 1:
                AALastRange = ''.join(set(AALastRange))
            if AAFirstRange == "-":
                AAFirstRange = "Ins"
            if AALastRange == "-":
                AALastRange = "Del"
            if len(Rangedf) > 1:
                Ranges.append(AAFirstRange + str(int(Rangedf['Positions'][0:1])) + "-" + str(int(Rangedf['Positions'][-1:])) + AALastRange)
            else:
                Ranges.append(AAFirstRange + str(int(Rangedf['Positions'][0:1])) + AALastRange)
        return Ranges

def AlignmentChangeFinderCleanup(df, FirstAA = 'Ref', FirstPositions = 'Ref'):
    
    """
    A function for cleaning up a pd.DataFrame produced by :func:`AlignmentChangeFinder`. It is a wrapper for the :func:`Rangemaker` function, which should be viewed for further explanation.

    Parameters
    ---
    df : A pd.DataFrame constructed by :func:`AlignmentChangeFinder`.
    
    FirstAA : Indicates which Ammino Acid should be shown for the result. Options include:

        'Ref' : Use the Ammino Acid indicated by (RefAA). Default option.

        'Majority' : Uses the most common Ammino Acid in the (Old) substring.

    FirstPositions : Indicates which positional marker should be shown for the result. Options include:

        'Ref' : Use the position from the (RefPos) substring. Does not include gaps. Default option.

        'Self' : Use the data in the (SelfPos) substring. Does not include gaps.

        'Align' : Use the data in the (AlignPos) substring.

    """

    import numpy as np
    import pandas as pd

    def list2Str(lst, FirstAA, FirstPositions):
        if type(lst) is list: # apply conversion to list columns
            return ", ".join(map(str, Rangemaker(lst, FirstAA, FirstPositions)))
        else:
            return lst
    
    df_clean = df.apply(lambda x: [list2Str(i, FirstAA, FirstPositions) for i in x]).replace(np.nan,"na") 

    return df_clean

def FastaListSplitter(FastaList):
    """
    A function designed to split a .fasta file into a pd.DataFrame consisting of each entry's id, Sequence, and Description.

    Parameters
    ---

    FastaList : A list of a Bio.SeqIO parse file. 
    >>> Example
    FastaList = list(SeqIO.parse(FastaFile, Format)) where Format = "Fasta"

    Returns
    ---

    A pd.DataFrame split into three columns. This function is part of :func:`FastaDescriptionHunter`.

    """
    import pandas as pd
    for i in range(len(FastaList)):
        id = str(FastaList[i].id)
        sequence = str(FastaList[i].seq)
        description = FastaList[i].description
        if i == 0:
            df = pd.DataFrame({'id': [id], 'Sequence': [sequence], 'Description': [description]})
        if i != 0:
            df.loc[len(df.index)] = [id, sequence, description]  
    df['id'] = df['id'].map(lambda x: x.split("_", 1)[0].replace('lcl|', ""))
    return df

def descriptioncontainssubs(description, descriptioncats, searchwords):
    """
    A function used to sort by two string filters as part of a .map function. Part of the :func:`FastaDescriptionHunter` function.

    Parameters
    ---

    description : List of strings to be searched. 
    
    descriptioncats : List of strings to search description for. Likely used for selecting categories.

    searchwords : List of strings to search elements selected by descriptioncats for containing.

    Returns
    ---

    A list of strings containing the portion of description contianing any searchwords.

    Examples
    ---
    >>> description
    [''. 'protein=major capsid protein VP72', 'protein_id=AAD49226.1', 'location=<1..>1915', 'gbkey=CDS']
    >>> descriptioncats
    ['gene','protein_id', 'product', 'protein']
    >>> searchwords
    ['p72', 'P72', 'b646', 'B646']

    These inputs would produce the following output:
    
    >>> output
    [protein=major capsid protein VP72]

    """
    import re
    def Filter(string, substr):
        return [str for str in string if any(sub in str for sub in substr)]
    
    return Filter(Filter(description, descriptioncats), searchwords)

def FastaDescriptionHunter(FastaFile, DescriptionTerms, SearchTerms, KeepAll = True):
    
    """
    This tool is used to find items in a .fasta file that contain one of particular phrases in part in certain portions of its description.

    Documentation for .fasta files can be found at https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ and examples provided at https://en.wikipedia.org/wiki/FASTA_format#Description_line.

    Parameters
    ---
    
    FastaFile : A string containing a path to a .fasta file.

    DescriptionTerms : A list of categories in descriptions to be searched. Case sensitive.
    >>> Example
    ['gene','protein_id', 'product', 'protein']

    SearchTerms : A list of what to search appropriate descriptions for. Case sensitive.
    >>> Example
    ['p72', 'P72', 'b646', 'B646']

    KeepAll = Determines if function returns all values, or only ones that are found. Default True.

    Returns
    ---
    A pd.Dataframe with 5 columns, the first three describe the id, sequence, and description of the entry. The final two describe any found description items and the length of found descriptions to allow further confirmation and processing.

    >>> example df output
        id          Sequence                Description             SearchTerms                         SearchTerms_L
    132 AF159503.1  CLIANDGKADKIILAQDL...   lcl|AF159503.1_prot_... [protein=major capsid protein VP72] 1
    133 AF159503.1  CLIANDGKADKIILAQDL...   lcl|AF159503.1_prot_... []                                  0
    """

    from Bio import SeqIO
    import pandas as pd

    FastaList = list(SeqIO.parse(FastaFile, format= 'fasta'))        
    dfFastaList = FastaListSplitter(FastaList)

    dfFastaList['SearchTerms'] = dfFastaList['Description'].map(lambda x: descriptioncontainssubs(x.replace(FastaList[0].id,"").replace("]", "").split(" ["),DescriptionTerms,SearchTerms))

    dfFastaList['SearchTerms_L'] = dfFastaList['SearchTerms'].map(lambda x: len(x))
    if KeepAll != True:
        dfFastaList = dfFastaList[dfFastaList['SearchTerms_L']>0].drop_duplicates('id')
    return dfFastaList

#Matrix/Cluster Section

def CSVToAllBanks(GenomicDF, DestinationFolder, musclepath, Seq = "Sequence", ID = "Genome", Grouping = "Gene", gapextpenalty = -1.0, gapopenpenalty = -10.0, CounterEnd = 15, CounterInterval = 0.1, StatsAsCSV = True):

    """
    This function does a full computation from a starting .csv to all the Banks available in this program. This includes :func:`MakeGeneBank`, :func:`GeneBankToAlignmentBank`, :func:`AlignmentBankToMatrixBank`, :func:`MatrixBankToClusterBank`, as well as :func:`MatrixBankStats`.

    Parameters
    ---
    GenomicDF : A pd.DataFrame or a string of a path to a .csv file featuring rows of Genes, Genomes, and Sequences.
    >>> Example
    Genome      Gene    Sequence
    A           a       MDHIAL...
    A           b       MQRSTY...
    B           a       MDHIIL...

    DestinationFolder : The path to a folder to place the outputs. The outputs will be folders themselves that will be placed in this folder.
    >>> Example
    'Folder\\Subfolder\\DestinationFolder'

    Seq : String, default "Sequence". The column of GenomicDF holding the sequence information.

    ID : String, default "Genome". The column of GenomicDF holding the Genomic information.

    Grouping : String, default "Gene". The column of the GenomicDF holding the Gene information.

    musclepath : String, default 'muscle3.8.31_i86win32.exe'. The path to the muscle.exe to be used.

    gapextpenalty : Negative Number, default -1.0. to be used for calculating 
    
    """

    import pandas as pd

    if type(GenomicDF) == pd.DataFrame:
        df = GenomicDF
    elif type(GenomicDF) == str:
        df = pd.read_csv(GenomicDF)

    bugdf = MakeGeneBank(df, DestinationFolder + '\\FastaBank', Seq, ID, Grouping)
    GeneBankToAlignmentBank(DestinationFolder + '\\FastaBank', DestinationFolder + '\\AlignmentBank', musclepath, gapextpenalty, gapopenpenalty)
    AlignmentBankToMatrixBank(DestinationFolder + '\\AlignmentBank', DestinationFolder + '\\MatrixBank')
    MatrixBankToClusterBank(DestinationFolder + '\\MatrixBank', DestinationFolder + '\\ClusterBank', CounterEnd, CounterInterval)
    DF_Stats = MatrixBankStats(DestinationFolder + '\\MatrixBank')
    if StatsAsCSV == True:
        DF_Stats.to_csv(DestinationFolder + '\\GeneMatrixStats.csv')   

    return DF_Stats, bugdf

def MatrixBankAverageMaker(dfnumber, dflength, dflist, OutputFolder, CriticalGeneList, NonCriticalWeightList, PenaltyList, MinGenomesList, CounterEnd = 15, CounterInterval = 0.1):
    
    """
    A wrapper for the :func:`MatrixDataToAverageMatrix` and :func:`MatrixToCluster` specifications to perform analysis on a wide variety of samples.
    
    Parameters
    ---
    dfnumber : returns a matrix, where each cell contains a list of the distances between two genomes across a number of genes.
    
    dflength : returns a matrix, where each cell contains a list of the number of genomes for each gene.
    
    dflist : returns a matrix, where each cell contains a list of the name of genes.
    
    OutputFolder : 
    
    CriticalGeneList : A list of a list of Strings, Default None. Use the name as defined by the name used in the .csv file. Items indicated here will not be modified by NonCriticalWeight.
    
    NonCriticalWeightList : A list of numbers, Default 1. Genes not in the CriticalGene list will have thier weight equal to this number. A weight of 0 means genes not in the CriticalGene will not be weighted.
    
    PenaltyList : A list of numbers, Default 0. This number modifies the weight of a gne by the number of genomes present in it by an exponent equal to the number. For instance, a value of 0.5 would multiply the weight of each gene by the square root of how many genomes it has.
    
    MinGenomesList : A list of numbers, Default 0. This number is the minimum number of genomes a gene must appear in before being considered.
    
    CounterEnd : 
    
    CounterInterval :
    
    Returns
    ---
    
    """
    
    import pandas as pd

    OutputFolder = FolderPathFixer(OutputFolder)

    CGGroup = 0
    for CriticalGene in CriticalGeneList:
        CGGroup += 1
        for NonCriticalWeight in NonCriticalWeightList:
            for Penalty in PenaltyList:
                for MinGenomes in MinGenomesList:
                        try:
                            DF_Average = MatrixDataToAverageMatrix(dfnumber, dflength, dflist, CriticalGene, NonCriticalWeight, Penalty, MinGenomes)
                        except:
                            print("CG" + str(CGGroup) + "_NCW" + str(NonCriticalWeight) + "_P" + str(Penalty) + "_MG" + str(MinGenomes) + " Failed on Average")
                            continue
                        try:
                            DF_Cluster = MatrixToCluster(DF_Average, CounterEnd, CounterInterval)
                        except:
                            print("CG" + str(CGGroup) + "_NCW" + str(NonCriticalWeight) + "_P" + str(Penalty) + "_MG" + str(MinGenomes)  + " Failed on Cluster")
                            continue
                        try:
                            DF_Average.to_csv(OutputFolder + "CG" + str(CGGroup) + "_NCW" + str(NonCriticalWeight) + "_P" + str(Penalty) + "_MG" + str(MinGenomes) + "_Average.csv")
                            DF_Cluster.to_csv(OutputFolder + "CG" + str(CGGroup) + "_NCW" + str(NonCriticalWeight) + "_P" + str(Penalty) + "_MG" + str(MinGenomes) + "_Cluster.csv")
                        except:
                            print("CG" + str(CGGroup) + "_NCW" + str(NonCriticalWeight) + "_P" + str(Penalty) + "_MG" + str(MinGenomes) + " Failed on Save")
                            continue

def AlignmentBankToMatrixBank(AlignmentBank, MatrixBank):

    """
    A wrapper of :func:`AlignmentToMatrix` that applies across a folder of .fasta alignment files and creates a corresponding folder of .csv distance matricies. The results of this function can be fed into further functions, such as :func:`MatrixBankToClusterBank` or :func:`MatrixBankToAverageMatrix` or :func:`MatrixBankStats`.

    Parameters
    ---

    AlignmentBank : String. The path to a folder holding .fasta alignment files, such as those created by :func:`GeneBankToAlignmentBank`
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\AlignmentBank'

    MatrixBank : String. A path to a folder, where the distance matricies for each gene will be contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank'

    Returns
    ---

    MatrixBank : A folder containing a series of .csv files containing the distance matrix between various geneomes for that gene.
    """

    import Bio.Phylo.TreeConstruction
    import pandas as pd
    import Bio.AlignIO
    import glob
    import Bio.SeqRecord

    AlignmentBank = FolderPathFixer(AlignmentBank)
    MatrixBank = FolderPathFixer(MatrixBank)
    
    my_files = glob.glob(AlignmentBank + '*')
    for fasta in my_files:
        try:
            df = AlignmentToMatrix(fasta)
            df.to_csv(fasta.replace(AlignmentBank, MatrixBank).replace(".fasta",".csv"))
        except:
            print("There was an error with " + fasta + " this could be caused due to having duplicate entries. Item skipped.")

            continue

def MatrixBankToClusterBank(MatrixBank, ClusterBank, CounterEnd = 15, CounterInterval = 0.1):

    """
    A wrapper of :func:`MatrixToCluster`. Transforms a folder of .csv files contianing distance matricies, such as a folder created by :func:`AlignmentBankToMatrixBank`, into a folder of .csv files organizing this matrix into clusters using the sklearn.cluster's DBSCAN method.

    Parameters
    ---
    MatrixBank : A path to a folder, where the distance matricies for each gene are contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank'

    ClusterBank : String. A path to a folder, where the cluster data for each gene are contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\ClusterBank'

    CounterEnd : Integer, default 15. How high the eps from DBSCAN should be calculated.

    CounterInterval : Float, default 0.1. At what intervals the DBSCAN eps should be calculated.

    Returns
    ---
    A folder where the cluster data for each gene are contained as .csv files.

    Example
    ---
    FastaTransformer.MatrixBankToClusterBank(MatrixBank = 'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank', ClusterBank='Project_AD-Unique Protein Sequences in new Genomes\ClusterBank')
    """

    import glob
    from sklearn.cluster import DBSCAN
    import pandas as pd

    MatrixBank = FolderPathFixer(MatrixBank)
    ClusterBank = FolderPathFixer(ClusterBank)
    
    my_files = glob.glob(MatrixBank + '*')
    for matrix in my_files:

        Final_DF = MatrixToCluster(matrix, CounterEnd, CounterInterval)
        ouputfasta = matrix.replace(MatrixBank, ClusterBank).replace(".fasta", ".csv")
        Final_DF.to_csv(ouputfasta)

def MatrixBankToMatrixData(MatrixBank):

    """
    Produces three pd.DataFrames that contain combined information of a folder of distance matricies, such as one produced by :func:`AlignmentBankToMatrixBank`. The returns of this file are primarily used in later calculations.
    
    Parameters
    ---
    MatrixBank : String. A path to a folder, where the distance matricies for each gene will be contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank'

    Returns
    ---
    dfnumber : returns a matrix, where each cell contains a list of the distances between two genomes across a number of genes.
    
    dflength : returns a matrix, where each cell contains a list of the number of genomes for each gene.
    
    dflist : returns a matrix, where each cell contains a list of the name of genes.
    
    """

    import pandas as pd
    import glob
    import Programs.FastaTransformer.src.FastaTransformer.FastaTransformer as FastaTranformer

    MatrixBank = FastaTranformer.FolderPathFixer(MatrixBank)
    my_files = glob.glob(MatrixBank + '*')
    
    GenomeList = []
    for file in my_files:
        dfactive = pd.read_csv(file, index_col=0)
        GenomeList.extend(list(dfactive.index))
    GenomeList = pd.unique(GenomeList)

    dfnumber = pd.DataFrame(index=GenomeList, columns=GenomeList)
    for item in dfnumber.index:
        dfnumber[item] = dfnumber[item].apply(lambda x: [])

    dflength = pd.DataFrame(index=GenomeList, columns=GenomeList)
    for item in dflength.index:
        dflength[item] = dflength[item].apply(lambda x: [])

    dflist = pd.DataFrame(index=GenomeList, columns=GenomeList)
    for item in dflist.index:
        dflist[item] = dflist[item].apply(lambda x: [])

    for file in my_files:

        dfactive = pd.read_csv(file, index_col=0)

        for item in dfactive.index:
            for name, row in pd.DataFrame(dfactive[str(item)]).iterrows():
                dfnumber[item][name].append(float(row.values))
                dflength[item][name].append(len(dfactive))
                dflist[item][name].append(file.replace(MatrixBank, "").replace(".csv",""))


    return dfnumber, dflength, dflist

def MatrixBankToAverageMatrix(MatrixBank, CriticalGene = None, NonCriticalWeight = 1, Penalty = 0, MinGenomes = 0):
    """
    A wrapper of :func:`MatrixBankToMatrixData` and :func:`MatrixDataToAverageMatrix`.
    
    Parameters
    ---
    
    MatrixBank : String. A path to a folder, where the distance matricies for each gene will be contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank'
    
    CriticalGene : List of Strings, Default None. Use the name as defined by the name used in the .csv file. Items indicated here will not be modified by NonCriticalWeight.
    >>> Example
    ['285L','B646L']

    NonCriticalWeight : A number, Default 1. Genes not in the CriticalGene list will have thier weight equal to this number. A weight of 0 means genes not in the CriticalGene will not be weighted.

    Penalty : A number, Default 0. This number modifies the weight of a gne by the number of genomes present in it by an exponent equal to the number. For instance, a value of 0.5 would multiply the weight of each gene by the square root of how many genomes it has.

    MinGenomes : A number, Default 0. This number is the minimum number of genomes a gene must appear in before being considered.
    
    Returns
    ---
    A pd.DataFrame of a distance matrix, with the distances being the weighted average of the matricies.
    
    """
    
    
    dfnumber, dflength, dflist = MatrixBankToMatrixData(MatrixBank)
    dfaverage = MatrixDataToAverageMatrix(dfnumber, dflength, dflist, CriticalGene, NonCriticalWeight, Penalty, MinGenomes)
    return dfaverage

def MatrixDataToAverageMatrix(MatrixNumbers, MatrixLengths, MatrixLists, CriticalGene = None, NonCriticalWeight = 1, Penalty = 0, MinGenomes = 0):

    """
    A function for generating an average matrix from a folder containing .csv matrix files such as one created by :func:`AlignmentBankToMatrixBank`. Returns a pandas DataFrame.

    Parameters
    ---
    MatrixNumbers : a matrix, where each cell contains a list of the distances between two genomes across a number of genes. Likely from :func:`MatrixBankToMatrixData`.
    
    MatrixLengths : a matrix, where each cell contains a list of the number of genomes for each gene. Likely from :func:`MatrixBankToMatrixData`.
    
    MatrixLists : a matrix, where each cell contains a list of the name of genes. Likely from :func:`MatrixBankToMatrixData`.
    
    CriticalGene : List of Strings, Default None. Use the name as defined by the name used in the .csv file. Items indicated here will not be modified by NonCriticalWeight.
    >>> Example
    ['285L','B646L']

    NonCriticalWeight : A number, Default 1. Genes not in the CriticalGene list will have thier weight equal to this number. A weight of 0 means genes not in the CriticalGene will not be weighted.

    Penalty : A number, Default 0. This number modifies the weight of a gne by the number of genomes present in it by an exponent equal to the number. For instance, a value of 0.5 would multiply the weight of each gene by the square root of how many genomes it has.

    MinGenomes : A number, Default 0. This number is the minimum number of genomes a gene must appear in before being considered.
    
    Returns
    ---
    A pd.DataFrame of a distance matrix, with the distances being the weighted average of the matricies.

    """
    
    import pandas as pd
    import numpy as np
    import ast

    dfaverage = pd.DataFrame(index=MatrixNumbers.index, columns=MatrixNumbers.index)
    for item in dfaverage.index:
        
        import numpy as np
        dfaverage[item] = dfaverage[item].apply(lambda x: [])
        
        #Weight for Being Critical
        if CriticalGene == None:
            CriticalGene = []


        dfpart1 = MatrixLists[item].apply(lambda x: [1 if i in CriticalGene else NonCriticalWeight for i in ast.literal_eval(x)])
        
        #0-1 Switch for Length
        dfpart2 = MatrixLengths[item].apply(lambda x: [i if i >= MinGenomes else 0 for i in ast.literal_eval(x)])
        dfpart2 = dfpart2.apply(lambda x: [i**Penalty if i > 0 else 0 for i in x])
        
        dfall = pd.concat([dfpart1,dfpart2],axis=1)
        dfall.columns = ['a', 'b']
        Weights = dfall.apply(lambda x: list(a*b for a,b in zip(x['a'], x['b'])), axis=1)
        dfall2 = pd.DataFrame(pd.concat([MatrixNumbers[item],Weights],axis=1))
        dfall2.columns = ['a', 'b']
        dfaverage[item] = dfall2.apply(lambda x: np.average(ast.literal_eval(x['a']), weights = x['b']), axis = 1) #np.average(x[0], weights = x[1])

    return dfaverage

def AlignmentToMatrix(fasta):

    """
    A wrapper of the :func:`Bio.Phylo.TreeConstruction.DistanceCalculator('identity').get_distance` function to take a .fasta alignment file and change it into a distance matrix. 

    Parameters
    ---
    fasta : The path to a .fasta file.

    Returns
    ---
    A pd.DataFrame of the alignment matrix.

    Example
    ---
    >>> df = AlignmentToMatrix("Project_AE_NewCaldes_02\AlignmentBank\A104R.fasta")
    """
            
    import Bio.SeqRecord
    import Bio.AlignIO
    import Bio.Phylo.TreeConstruction
    import pandas as pd
    import Bio.SeqIO

    with open(fasta) as fasta_file:
        New_Record = []
        for seq_record in Bio.SeqIO.parse(fasta_file, 'fasta'):
            New_Record.append(Bio.SeqRecord.SeqRecord(seq_record.seq, id = seq_record.description.replace(" ","###")))

        matrix = Bio.Phylo.TreeConstruction.DistanceCalculator('identity').get_distance(Bio.AlignIO.MultipleSeqAlignment(New_Record))
        names = [i.replace('###', ' ') for i in matrix.names]
        df = pd.DataFrame(list(matrix), columns=names, index=names)
        df = df.apply(lambda x: 1-x)
    
    return df

def MatrixToCluster(Matrix, CounterEnd = 15, CounterInterval = 0.1):

    """
    Parameters
    ---

    Matrix : String of Path to a .csv file containing a distance matrix, or a pd.DataFrame of the matrix.

    CounterEnd : Integer, default 15. How high the eps from DBSCAN should be calculated.

    CounterInterval : Float, default 0.1. At what intervals the DBSCAN eps should be calculated.

    Returns
    ---
    A pd.DataFrame of the clusters.

    Example
    ---
    Final_Df = MatrixToCluster("Project_AE_NewCaldes_02\distancetestnopenalty.csv")
    """

    import pandas as pd
    from sklearn.cluster import DBSCAN
    import numpy as np
    
    if type(Matrix) == str:
        Matrix = pd.read_csv(Matrix, index_col=0)
    
    Isolates = Matrix.index.to_list()
    df2 = Matrix.reset_index().drop(['index'],axis=1)
    df2.columns = range(1, df2.shape[1]+1)
    df2.index += 1
    #
    clusterlist = []
    counterlist = []
    #
    Counter = CounterInterval
    while Counter <= CounterEnd:
        Counter = round(Counter, 2)
        db = DBSCAN(eps=Counter, min_samples=1).fit(df2)
        clusterlist.append(db.labels_)
        counterlist.append(Counter)
        Counter += CounterInterval

    return pd.DataFrame(np.array(clusterlist), columns=Isolates, index=counterlist).transpose()

def MatrixBankStats(MatrixBank):
    """
    Find the statistics of each gene in a folder of distance matricies, such as one produced by :func:`AlignmentBankToMatrixBank`.
    
    Parameters
    ---
    MatrixBank : A path to a folder, where the distance matricies for each gene are contained as .csv files.
    >>> Example
    'Project_AD-Unique Protein Sequences in new Genomes\MatrixBank'
    
    Returns
    ---
    A pd.DataFrame consisting of the mean, median, standard deviation and number of genomes in each genes difference matrix.
    """
    import pandas as pd
    import glob
    import numpy as np
    DF_Stats = pd.DataFrame(columns=['Mean', 'Median', 'StdDev', 'Count'])
    MatrixBank = FolderPathFixer(MatrixBank)
    my_files = glob.glob(MatrixBank + '*')
    for file in my_files:
        Numbers = []
        dfactive = pd.read_csv(file, index_col=0)
        for item in dfactive.index:
            Numbers.extend(list(dfactive[str(item)].values))
            Numbers.remove(1)
        DF_Stats.loc[str(file.replace(MatrixBank, "").replace(".csv",""))] = [np.mean(Numbers), np.median(Numbers), np.std(Numbers), int(len(dfactive))]
    return DF_Stats