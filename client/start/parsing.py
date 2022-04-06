from utilities.utils import log, run_checks
import json
import utilities.esvutil as esvutil
import certifi
import globalenv

#Parse the config file into usable variables
def parse_config(config_path):
    
    try:
        config = open(config_path, 'r')
        config = json.load(config)

        client_cert = (config[0]['CertPath'], config[0]['KeyPath'])
        log("client_cert", client_cert)
        seed_path = config[0]['TOTPPath']
        server_url = config[0]['ServerURL']
        esv_version = config[0]['EsvVersion']
        log("server_url", server_url)
        '''
        singleMod = config[2]['limitEntropyAssessmentToSingleModule']
        modId = None; vendId = None; oeId = None

        certify = config[1]['Certify'] 
        if certify: #Certification requires module and vendor IDs
            try:
                modId = config[1]['moduleID']
                vendId = config[1]['vendorID']
            except:
                print("Error: Module and Vendor IDs are required for certification")
                exit()
        
        if certify and config[2]['numberOfAssessments'] == 1: #Certifying only 1 assessment requires oeID
            try:
                oeId = config[2]['oeID']
            except:
                print("Error: oeID field needed when certifying 1 assessment")
                exit()
'''
        if(globalenv.verboseMode):
            print("Config file successfully parsed")
        return client_cert, seed_path, server_url, esv_version # modId, vendId, oeId, certify, singleMod
    except Exception as e:
        print("There was an error parsing your config file. Please try again")
        print(e)


        exit()

#Parse the run file into usable variables
def parse_run(run_path):
    try:
        run_file = open(run_path, 'r')
        run_file = json.load(run_file)
        assessment_reg = esvutil.loadObject(run_file[0]["AssessmentRegistrationPath"])
        rawNoise = run_file[0]["DataFiles"]["rawNoisePath"]
        restartTest = run_file[0]["DataFiles"]["restartTestPath"]
        conditioned = run_file[0]["DataFiles"]["unvettedConditionedPaths"] #need to take sequence position into account
        supporting_paths = run_file[0]["SupportingDocuments"]["filePaths"]
        comments = run_file[0]["SupportingDocuments"]["comments"]
        run_checks(comments, supporting_paths)

        singleMod = run_file[0]["Assessment"]['limitEntropyAssessmentToSingleModule']
        modId = None; vendId = None; oeId = None

        certify = run_file[0]["Certify"]['Certify'] 
        if certify: #Certification requires module and vendor IDs
            try:
                entropyId = run_file[0]["Certify"]['entropyID']
                modId = run_file[0]["Certify"]['moduleID']
                vendId = run_file[0]["Certify"]['vendorID']
            except:
                print("Error: Entropy, Module and Vendor IDs are required for certification")
                exit()
        
        if certify and run_file[0]["Assessment"]['numberOfAssessments'] == 1: #Certifying only 1 assessment requires oeID
            try:
                oeId = run_file[0]["Assessment"]['oeID']
            except:
                print("Error: oeID field needed when certifying 1 assessment")
                exit()

        entr_jwt = run_file[0]["PreviousRun"]["entr_jwt"]
        df_ids = run_file[0]["PreviousRun"]["df_ids"]
        ea_id = run_file[0]["PreviousRun"]["ea_id"]
        cert_supp = run_file[0]["PreviousRun"]["cert_supp"]
        if(globalenv.verboseMode):
            print('Run file successfully parsed')
        return assessment_reg, rawNoise, restartTest, conditioned, supporting_paths, comments, modId, vendId, entropyId, oeId, certify, singleMod, entr_jwt, df_ids, ea_id, cert_supp

    except:
        print("There was an error parsing your run file. Please try again")
        exit()

def parse_certify_response(response):
    response = response.json()
    status = response[1]['status']
    messageList = response[1]["information"]["messageList"]
    elementList = response[1]["information"]["entropyAssessmentsReferences"]["elementList"]
    return status, messageList, elementList