# ECOLOPES Project - WP5 - Computational model and Voxel model
 
## This repository contains code for the following project deliverables:
1. D5.1 ECOLOPES Voxel model (@themanoftalent)  
2. D5.2 ECOLOPES Computational model in Rhino3D (@themanoftalent)  

## T5.1 ECOLOPES Voxel model (@themanoftalent)
Task descritpion:  
*Task 5.1: ECOLOPES Voxel Model, Development of a voxel model as a link between EIM Ontology (WP4) and computational model. The voxel model will contain different types of data. The geometric data in the voxel model provides the link to the computational model in Rhino3D. Tangible outcome: ECOLOPES Voxel model(D5.1).*  
  
According to project schedule, the deliverable related to the ECOLOPES Voxel Model is:  
  
D5.1 - Demonstrator - *to be submitted in September 2023*  
D5.1 - Written report - *to be submitted in September 2023* @MH: we have to submit some text, right?  
  
## T5.2 ECOLOPES Computational model in Rhino3D (@themanoftalent)  
  
Task descritpion:  
*Development and integration of algorithmic processes and tools for the design of ECOLOPES in Rhino3D leading to the ECOLOPES  Computational  Model. This will be related to work on the design cases for Munich, Vienna, Genoa and Haifa. Tangible outcome: Algorithmic processes and tools.*  

According to project schedule, the deliverable related to the ECOLOPES Computational model is:  

D5.2 -  Demonstrator - ECOLOPES Computational model in Rhino3D - *to be submitted in September 2023*  
D5.2 -  Written report - ECOLOPES Computational model in Rhino3D - *to be submitted in September 2023* @MH: we have to submit some text, right?  

### ECOLOPES WP5 Workplan:
According to the Ecolopes Workplan set by Micahel Hensel (MH) on 06.02.2023 this repository contains code for the *second line of development*:  

(MH) As you have seen I have organised the next steps so as to proceed alo ng two lines of development:  
1. Networks & Ontology / Knowledge Graph 1: Defne, Tina and Albin  
2. Volumes & Ontology / Knowledge Graph 2:  Akif and me (@MH)  

\(\.\.\.\)

In detail, the second line of development consists of:  
2\. Volumes & Ontology / Knowledge Graph 2:  
I (MH) will lead this group  
Akif (@themanoftalent) and I (@MH) will develop the approach to the ontology / knowledge graph  
 (@themanoftalent) and Akif (@themanoftalent) will develop the link to and interface in Grasshopper  

## ECOLOPES project description as understood by Akif (@themanoftalent)
ECOLOPES is a project focusing on developing a voxel model and generative process. It is a collaboration between  Tyc (@themanoftalent) and Mehmet Akif CIFCI (@themanoftalent).

The main goal of this project is to create a tool that can generate 3D models from a set of parameters and process existing models. The voxel model is based on a grid of small cubes and represents 3D shapes in a digital format. This makes it easy to create, modify, and manipulate complex models.

The generative process involves creating a set of rules that determine how the voxel model should be generated. This allows for a high degree of customization and control over the final product. The user can specify parameters such as the overall shape, size, and details of the model. The generative process then takes these parameters into account and produces a unique model based on them.

The code for this project is open source and available on GitHub, making it easy for developers and users to access and contribute to the project. We believe that the ECOLOPES project has the potential to be a valuable tool for those interested in 3D modeling, and we are excited to see where the community takes it.

This repository is a combination of  Tyc's Hops/Pyinstaller template code and the work of Mehmet Akif Ciftci (themanoftalent). At this moment, all the code is in one merged repository, but the option to split it into separate repositories in the future is available if necessary.

  
## Quickstart
1. you need Python, tested on >= 3.10  
   tested on 3.10 Win and Linux (Ja-Ty) and MacOS (themanoftalent)  
2. create new virtualenv or anaconda env  
3. install numpy with pip (!)  
   please, no numpy from anaconda, it is packaged with 700MB MKL library -> bad for Pyinstaller  
4. install requrements from the requiremetns.txt file  
   with pip -> pip install -r /path/to/requirements.txt  
   with coda -> (...) *TODO / DOKU*
   

on Windows:  
- you can run the 00_run_venv.bat file to run the code  
or 
- or you can build the .exe file with 00_build_pyinst.bat

on nix:
*TODO / DOKU*

### TODO:
- [ ] regenerate requirements.txt when we are done with Akifs components:  
      pipreqs /path/to/project  
   
- [x] separate directory for docs (/doc) + our .md files  
      following the four main sections structure  
      tutorials / how-to / references / explanations  
      we have now mostly references, right?  
      see https://realpython.com/documenting-python-code/#the-four-main-sections-of-the-docs-folder  
- [ ] make some notebooks to quickly test the code + make a dir for them  
      possibly under /doc/how-to  
- [ ] write some tests + make a dir for them  
- [ ] write dummy map data + make dir for it    
- [ ] (...)  
