#Requests library for accessing jenkins rest api
import requests
from requests.auth import HTTPBasicAuth 
#To supress warning message from console log output using warnings library
import warnings
#Creating a xml config file using Etree library
import xml.etree.ElementTree as ET
from lxml import etree

warnings.filterwarnings("ignore")
#Defining the headers of the request as xml 
headers = {'Content-Type':'application/xml'}

def create_config(dict_parameters):
    data = ET.Element('flow-definition')
    data.set('plugin',"workflow-job@2.38")
    sub_elem_action = ET.SubElement(data,"actions")
    sub_elem_declarativejobaction = ET.SubElement(sub_elem_action,"org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction")
    sub_elem_declarativejobaction.set("plugin","pipeline-model-definition@1.6.0")
    sub_elem_declarativejobpropertytrackeraction = ET.SubElement(sub_elem_action,"org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction")
    sub_elem_declarativejobpropertytrackeraction.set("plugin","pipeline-model-definition@1.6.0")
    sub_elem_jobproperties = ET.SubElement(sub_elem_declarativejobpropertytrackeraction,"jobProperties")
    sub_elem_triggers  = ET.SubElement(sub_elem_declarativejobpropertytrackeraction,"triggers")
    sub_elem_parameters  = ET.SubElement(sub_elem_declarativejobpropertytrackeraction,"parameters")
    sub_elem_options  = ET.SubElement(sub_elem_declarativejobpropertytrackeraction,"options")
    sub_elem_descr = ET.SubElement(data,"description")
    sub_elem_descr.text = ""
    sub_elem_kdependecy = ET.SubElement(data,"keepDependencies")
    sub_elem_kdependecy.text = "false"
    
    sub_elem_properties = ET.SubElement(data,"properties")
    '''    
    #Incase any input parameter to be defined in our Jenkins job
    sub_elem_parameters_property = ET.SubElement(sub_elem_properties,"hudson.model.ParametersDefinitionProperty")
    sub_elem_property_definition = ET.SubElement(sub_elem_parameters_property,"parameterDefinitions")
    sub_elem_string_definition = ET.SubElement(sub_elem_property_definition,"hudson.model.StringParameterDefinition")
    sub_elem_name = ET.SubElement(sub_elem_string_definition,"name")
    sub_elem_name.text = dict_parameters['parameter_name']
    sub_elem_parameter_description = ET.SubElement(sub_elem_string_definition,"description")
    sub_elem_parameter_default = ET.SubElement(sub_elem_string_definition,"defaultValue")
    sub_elem_trim = ET.SubElement(sub_elem_string_definition,"trim")
    sub_elem_trim.text = "false"
    '''
    sub_elem_definition = ET.SubElement(data,"definition")
    sub_elem_definition.set("class","org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition")
    sub_elem_definition.set("plugin","workflow-cps@2.80")
    
    sub_elm_scm = ET.SubElement(sub_elem_definition,"scm")
    sub_elm_scm.set("class","hudson.plugins.git.GitSCM")
    sub_elm_scm.set("plugin","git@4.3.0")
    sub_elm_configversion = ET.SubElement(sub_elm_scm,"configVersion")
    sub_elm_configversion.text="2"
    sub_elm_user_configs  = ET.SubElement(sub_elm_scm,"userRemoteConfigs")
    sub_elm_git = ET.SubElement(sub_elm_user_configs,"hudson.plugins.git.UserRemoteConfig")
    sub_elm_url = ET.SubElement(sub_elm_git,"url")
    sub_elm_url.text = dict_parameters['git_url']
    sub_elm_credid = ET.SubElement(sub_elm_git,"credentialsId")
    sub_elm_credid.text = dict_parameters['git_cred_id']
    sub_elm_branches = ET.SubElement(sub_elm_scm,"branches")
    sub_elm_hudson_branch = ET.SubElement(sub_elm_branches,"hudson.plugins.git.BranchSpec")
    sub_elm_hudson_branch_name = ET.SubElement(sub_elm_hudson_branch,"name")
    sub_elm_hudson_branch_name.text = "*/${"+dict_parameters['parameter_name']+"}"
    sub_elm_do_generate_subs = ET.SubElement(sub_elm_scm,"doGenerateSubmoduleConfigurations")
    sub_elm_do_generate_subs.text = "false"
    sub_elm_submodule = ET.SubElement(sub_elm_scm,"submoduleCfg")
    sub_elm_submodule.set("class","list")
    sub_elm_extension = ET.SubElement(sub_elm_scm,"extensions")
    #Incase you have sub folders to access from your git repo, use sparse checkout
    sub_elm_hudson_sparse = ET.SubElement(sub_elm_extension,"hudson.plugins.git.extensions.impl.SparseCheckoutPaths")
    sub_elm_sparse = ET.SubElement(sub_elm_hudson_sparse,"sparseCheckoutPaths")
    sub_elm_extension_sparse = ET.SubElement(sub_elm_sparse,"hudson.plugins.git.extensions.impl.SparseCheckoutPath")
    sub_elm_path_sparse = ET.SubElement(sub_elm_extension_sparse,"path")
    sub_elm_path_sparse.text = dict_parameters['sparse_checkout']
    
    #Script path is the place of the Jenkinsfile path in the git
    sub_elm_scriptpath = ET.SubElement(sub_elem_definition,"scriptPath")
    sub_elm_scriptpath.text = dict_parameters['jenkins_file']

    sub_elm_lightweight = ET.SubElement(sub_elem_definition,"lightweight")
    sub_elm_lightweight.text = "false"

    sub_elem_triggers  = ET.SubElement(data,"triggers")
    sub_elem_disabled = ET.SubElement(data,"disabled")
    sub_elem_disabled.text = "false"
    
    b_xml = ET.tostring(data)
    tree = etree.fromstring(b_xml.decode("utf-8"))
    xml = etree.tostring(tree, encoding="unicode", pretty_print=True)
    create_job(dict_parameters['job_name'],xml)
    
def create_job(job_name,xml):
    jenkins_url = ""
    response = requests.post(jenkins_url+job_name,data =xml,verify = False,
                    auth = HTTPBasicAuth(username, password),
                    headers=headers
                    )
    print("Job status:- ",response.reason,response)

def code_startup(dict_parameters):
    print("Creating Jenkins a job:- ",dict_parameters['job_name'])
    create_config(dict_parameters) #Creates an apply job in jenkins
    dict_parameters.clear()

if __name__ == "__main__":
    dict_parameters = {}
    input_parameter_name = "example" #Incase you require parameters to e added in your jenkins job
    git_url = "example-repo-url"
    git_credential_id = "example-git-credential-id-in-jenkins" #if git credential is masked in jenkins credntial id
    jenkins_job_name = "example-job"
    jenkinsFile_path = "example/JenkinsFile"
    dict_parameters.update({
        "parameter_name" : input_parameter_name,
        "git_url" : git_url,
        "git_cred_id" : git_credential_id,
        "job_name" : jenkins_job_name,
        "sparse_checkout":sparse_checkout_path,
        "jenkins_file":jenkinsFile_path
        })
    code_startup(dict_parameters)