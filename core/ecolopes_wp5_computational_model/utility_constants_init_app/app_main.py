#SoftAiyazilim.com

import logging

from .constants import LOG_LVL, FLASK_HOSTNAME, VOX_DOC_PATH, HEVC_PATH

from .components.vox_read import *
from .components.vox_write import *

from .components.gen_random import *

#TODO: where to init the logger not to get the circular imports problem
#TODO: logggers in packages...

def main():

    print(f'Your data path is "{VOX_DOC_PATH}"')
    print(f'Using voxel data saved in "{VOX_FILENAME}"')
    print()

    #logging.basicConfig(filename="./newfile.log",
    #                    format='%(asctime)s %(message)s',
    #                    filemode='w')

    # we might need instantiate logger somewhere else, to use it in the
    # components and don't have circular imports...

    # Creating an object
    logger = logging.getLogger()

    #Add flask logger
    #logger.addHandler(default_handler)


    logger.setLevel(LOG_LVL)
    logger.info(f"Starting...")

    #logger.debug("Harmless debug Message")
    #logger.info("Just an information")
    #logger.warning("Its a Warning")
    #logger.error("Did you try to divide by zero")
    #logger.critical("Internet is down")


    ###

    #app_eng = Flask(__name__) 

    #app_eng.debug = True
    #app_eng.config['TEMPLATES_AUTO_RELOAD'] = True

    #@app_eng.route('/') 
    #def hello_world(): 
        #return 'Flask is great!'
        #return render_template('index.html')

    ###

	# wrapping Flask with Hops 
    # this needs to be passed to each component
    # for the decorator to work and the component to register
    # damn it doesnt work...
    # hops = hs.Hops(app_eng)

    ##let's try hops without the middleware
    hops = hs.Hops()

    ## This is dynamic loading of Hops components from submodules...

    #this is voxel specific, because we use "vox_"
    vox_comps = {k:v for k, v in globals().items() if k.startswith('vox_')}
    for (key, value) in vox_comps.items():
        if callable(value): #is_function
            try:
                kwargs = vox_comps[f'{key}_kwargs']
                func = vox_comps[f'{key}']
                hops.component(**kwargs)(func)
            except KeyError:
                logger.warning(f"Kwargs missing for function {vox_comps[key]}. " \
                        "Define them in the same file as the function")
                pass


    # I know this is a dirty hack...
    #TODO: generalize this block of code, so that it loads everything
    # from the /app/components/* and does the basic checking
    # modify the imports in this module to load eveything from components

    #this is generative process specific, because we use "gen_"
    gen_comps = {k:v for k, v in globals().items() if k.startswith('gen_')}
    for (key, value) in gen_comps.items():
        if callable(value): #is_function
            try:
                kwargs = gen_comps[f'{key}_kwargs']
                func = gen_comps[f'{key}']
                hops.component(**kwargs)(func)
            except KeyError:
                logger.warning(f"Kwargs missing for function {gen_comps[key]}. " \
                        "Define them in the same file as the function")
                pass

    #set host to '0.0.0.0' for external access
    ##app_eng.run(host=FLASK_HOSTNAME, port=engine_port)

    #import waitress

    engine_port = 5478
    logger.info(f"Runing Engine on: {engine_port}")

    for item in hops._components:
        print(f'http://{FLASK_HOSTNAME}:{engine_port}{item}')


    try:
        #set host to '0.0.0.0' for external access
        #app_eng.run(host=FLASK_HOSTNAME, port=engine_port)

        #this works without the middleware and fixes the problem with refreshing components
        hops.start(port=engine_port, debug=False)

        # ...and it can not run in production environment, yeah... 
        #waitress.serve(hops, host=FLASK_HOSTNAME, port=engine_port, threads=4) 

        #app_iter = self.channel.server.application(environ, start_response)
        #TypeError: 'HopsDefault' object is not callable

        #TODO: set the thread count externally 
        #waitress.serve(app_eng, host=FLASK_HOSTNAME, port=engine_port, threads=4)

    except KeyboardInterrupt:
        print()
        print('[Closing] KeyboardInterrupt - known bug in hopsdefault.py - just ignore...')
        pass
        

    ## TODO: think what to do about the thread safety of the SQL engine
    ## TODO: this is currently solved in Grasshopper by connecting all components
    ## TODO: with the vox_lvl_name input/output -> Grasshopper runs those components
    ## TODO: sequentially and the race conditions does not occur 