#Imported TSV file
def ImportTsv(tsv, nosubpositions = False):
    """
    A program for importing tsv files into an understandable and usable format. For understanding a tsv file see https://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/current/User_Manual.pdf, page 1119.
    
    Parameters
    ---
    tsv : a string that is the path to a .tsv file.
    
    nosubpositions : Boolean, default False. If True will on select items without subpositions.
    
    Returns
    ---
    A pd.DataFrame
    
    """
    import pandas as pd
    df = pd.read_csv(str(tsv), sep = '\t', names = ["RefName", "RefPosition", "RefSubPosition", "RefSymbol", "Num_A", "Num_C", "Num_G", "Num_T", "Num_N", "Num_Gap", "Total_Reads"])
    if nosubpositions == True:
        df[df['RefSubPosition'] == '-']
    return df
    
def CigarQualityConverter(string):
    """
    Take a quality string, such as those featured in a .sam or .fastq file, and turn them into a numerical representation of quality.
    
    Parameters
    ---
    A quality string.
    
    Returns
    ---
    A list of quality scores.
    
    """
    listOrd = []
    if string != "N/A":
        for character in string:
            listOrd.append(ord(character))
    else:
        listOrd == ["N/A"]
    return listOrd

def CigarConverter(SamLine, consumes_read = "MIS=X", consumes_consensus = "MDN=X"):
    
    """
    
    """
    
    import pandas as pd
    RefPositionList = []
    Sequence = ""
    Quality = ""
    ReadEaten = 0
    RefPositionStart = SamLine.pos

    CigarSequence = []
    CigarPosiiton = []
    CigarLength = []
    CigarType = []
    CigarQuality = []
            
    for cigar_length, cigar_type in SamLine.cigars:

        #Sequence and Quality
        if cigar_type in consumes_read:
            Sequence += SamLine.seq[ReadEaten:ReadEaten+cigar_length]
            CigarSequence.append(Sequence[-cigar_length:])
            Quality += SamLine.qual[ReadEaten:ReadEaten+cigar_length]
            CigarQuality.append(Quality[-cigar_length:])
            ReadEaten += cigar_length
        else:
            Sequence += (cigar_length*"-")
            CigarSequence.append("N/A")
            Quality += (cigar_length*"日")
            CigarQuality.append("N/A")
        
        if cigar_type in consumes_consensus:
            RefPositionList.extend(range(RefPositionStart,RefPositionStart+cigar_length))
            CigarPosiiton.append(RefPositionList[-cigar_length:])
            RefPositionStart += cigar_length
        else:
            RefPositionList.extend(cigar_length*[RefPositionStart])
            if len(CigarPosiiton) == 0:
                CigarPosiiton.append(RefPositionStart)
            else:
                CigarPosiiton.append(RefPositionStart-1)

        CigarType.append(cigar_type)
        CigarLength.append(cigar_length)

    #CigarList
    df_cigar = pd.DataFrame()
    df_cigar['Type'] = CigarType
    df_cigar['Length'] = CigarLength
    df_cigar['Sequence'] = CigarSequence
    df_cigar['RefPosition'] = CigarPosiiton
    df_cigar['Quality'] = CigarQuality

    
    
    df_cigar['QualityNum'] = df_cigar["Quality"].map(lambda x: CigarQualityConverter(x))

    #FullList
    #df = pd.DataFrame()
    #df['Sequence'] = list(Sequence)
    #df['ReferencePosition'] = RefPositionList
    #df['Cigar'] = CigarList
    #df['Quality'] = list(Quality)

    return df_cigar # df, removed due to being unused

def SamBreaker(sam, bugcheck = False):
    import simplesam
    import pandas as pd

    #Imported SAM file
    sam_iterator = simplesam.Reader(open(str(sam)))
    #For Help Understanding SAM files see https://genome.sph.umich.edu/wiki/SAM 
    # and https://samtools.github.io/hts-specs/SAMv1.pdf page 8
    
    df_Substitute = pd.DataFrame(columns=['Name', 'Type', 'Length', 'Sequence', 'RefPosition', 'Quality', 'QualityNum', 'Position'])
    
    for sam_current in sam_iterator:
        if bugcheck == True:
            print(sam_current.qname)
        df_cigar = CigarConverter(sam_current)     
        df_cigar['Position'] = 'Internal'
        df_cigar.at[0, 'Position'] = 'Start'
        df_cigar.at[len(sam_current.cigars)-1, 'Position'] = 'End'        
        df_cigar['Name'] = sam_current.qname
        df_cigar.insert(0,'Name', df_cigar.pop('Name'))
        
        df_Substitute = pd.concat([df_Substitute, df_cigar], ignore_index=True)
    
    return df_Substitute

def ClippingSummarize(df, includeposition = True):
    import pandas as pd
    import numpy as np

    df_S = df[df['Type']=='S']
    df_S['QualityNum'] = df_S['QualityNum'].map(lambda x: np.mean(x))
    if includeposition == True:
        df_S_Groups = pd.DataFrame(df_S.groupby(['RefPosition', 'Position'])['Name'].apply(list))
        df_S_Groups['Count'] = df_S.groupby(['RefPosition', 'Position'])['Name'].count()
        df_S_Groups['AverageLength'] = df_S.groupby(['RefPosition', 'Position'])['Length'].mean().values
        df_S_Groups['AverageQuality'] = df_S.groupby(['RefPosition', 'Position'])['QualityNum'].mean().values

    if includeposition == False:
        df_S_Groups = pd.DataFrame(df_S.groupby(['RefPosition'])['Name'].apply(list))
        df_S_Groups['Count'] = df_S.groupby(['RefPosition'])['Name'].count()
        df_S_Groups['AverageLength'] = df_S.groupby(['RefPosition'])['Length'].mean().values
        df_S_Groups['AverageQuality'] = df_S.groupby(['RefPosition'])['QualityNum'].mean().values

    return df_S_Groups.reset_index()

def ClippingSummarizeTSV(SamBreakerDf, TSV):
    df_tsv = ImportTsv(TSV, nosubpositions = True)
    if type(SamBreakerDf) == type('Str'):
        df_sam = SamBreaker(SamBreakerDf)
        df_Clipping = ClippingSummarize(df_sam)
    else:
        df_Clipping = ClippingSummarize(SamBreakerDf) 
    df_S_Groups = df_Clipping.merge(df_tsv, on = ['RefPosition'])
    df_S_Groups['PercentReads'] = df_S_Groups['Count']/df_S_Groups['Total_Reads']
    df_S_Groups = df_S_Groups[['RefPosition', 'Position',  'Count', 'AverageLength',  'AverageQuality', 'Total_Reads', 'PercentReads', 'Name']]
    if type(SamBreakerDf) == type('Str'):
        return df_sam, df_S_Groups
    return df_S_Groups

#Part 1
#df = SamBreaker(sam = 'UnalignedReadFinder/Ghana_35_Minion_R0 mapping.sam')
#df.to_csv('UnalignedReadFinder/Ghana_35_Minion_R0_sambreakdown.csv')

#import pandas as pd

#type(df) == type('Str')

#df_S_Groups = ClippingSummarizeTSV(df,'UnalignedReadFinder/Ghana_35_Minion_R0 mapping.tsv')
#df_sambreaker, df_S_Groups = ClippingSummarizeTSV('UnalignedReadFinder/Ghana_35_Minion_R0 mapping.sam','UnalignedReadFinder/Ghana_35_Minion_R0 mapping.tsv')
#df_S_Groups.to_csv('UnalignedReadFinder/Ghana_35_Minion_R0_sambreakdown_Sonly.csv', index=False)

#SamBreakerDf = 'UnalignedReadFinder/Ghana_35_Minion_R0 mapping.sam'
#TSV = 'UnalignedReadFinder/Ghana_35_Minion_R0 mapping.tsv'

#WTF did the graph go?!