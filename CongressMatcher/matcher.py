import os
import pandas as pd

def master_congress_merger(path, filename, lastname=None, firstname= None, state= None, congress = None, committee=None, body = None):

    """Takes some subset of data about a MOC and finds their bioguide id. Not
    the most efficient, but it is flexible to a wide variety of circumstances.
    
    Takes a path for the updated version of the HS_all file from Poole and Rosenthal with Committee Codes merged in. """
    
    #import the HS_all file- drop before 74
    os.chdir(path)
    with open(filename) as f:
        all_mems = pd.read_csv(f)
    
    all_mems = all_mems[all_mems['congress']>73]
    
    all_mems['lastname']  = [x.split(" ")[0][:-1] for x in all_mems['bioname']]
    all_mems['firstname'] = [x.split(" ")[1] for x in all_mems['bioname']]
    
    df = all_mems

    if committee != None: # Manually subsets the dataframe by the committee
        committee = str(committee)
        df['committees'] = df['committees'].fillna(0)
        LOLS = df['committees'].to_list()
        boolean=[]
        for item in LOLS:
            try:
                if committee in item:
                    boolean.append(True)
                else:
                    boolean.append(False)
            except:
                if committee == item:
                    boolean.append(True)
                else:
                    boolean.append(False)
        df = df[boolean]

      if congress!=None:
          matches = all_mems[ all_mems['congress'] == congress]
          df = matches.drop_duplicates(['bioguide_id'])

      if lastname != None:
          matches2 = df[ df['lastname'] == lastname.upper()]
          df = matches2.drop_duplicates(['bioguide_id'])

      if firstname != None:
          name_matches = df[df['firstname'] == firstname ]
          df = name_matches.drop_duplicates(['bioguide_id'])

      if state != None:
          state_matches =  df[df['state_abbrev'] == state ]
          df = state_matches.drop_duplicates(['bioguide_id'])

      if body != None:
          body_matches =  df[df['chamber'] == body]
          df = body_matches.drop_duplicates(['bioguide_id'])

      if len(df)>1:
          print("Unable to resolve the observation with given data. Current length of dataframe: " + str(len(df)))

      if len(df)<1:
          print("Information you entered in conflicted or inaccurate, please check your information and try again")
    
    return df

