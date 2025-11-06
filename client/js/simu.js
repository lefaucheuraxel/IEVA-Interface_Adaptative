
import {createPointerLock} from './utils/pointerLock.js' ; 
import {PRIMS} from './utils/prims.js' ; 
//import {Fabrique} from './fabrique.js' ; 
import {COMPS} from './composants/components.js' ; 
import {ActorManager} from './entites/actorManager.js' ; 
import {ACTORS} from './entites/actor.js';
import {loadJSON} from './load.js' ; 




class Simu {

	constructor(idCanvas){
    		this.canvas = document.getElementById(idCanvas);
    		this.engine = new BABYLON.Engine(this.canvas, true);
    		this.clock = 0.0; 


    		this.actorManager = new ActorManager({},this);

    		this.focus = null ; 

    		this.scene = new BABYLON.Scene(this.engine);
    		this.scene.useRightHandedSystem = false;
    		this.scene.gravity = new BABYLON.Vector3(0,-0.4,0) ; 
    		createPointerLock(this.scene);
    
    		this.gui = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI-Monde");

    		this.camera = PRIMS.camera("cam",{}, this.scene);
            this.boundingSphere = BABYLON.MeshBuilder.CreateSphere("boundingCamera",{diameter:1},this.scene) ; 
            this.boundingSphere.parent = this.camera ;
            this.boundingSphere.isVisible = false ; 
            this.boundingSphere.isPickable = false ; 
            this.boundingSphere.checkCollisions = false ; 
            

    
    		this.reticule = PRIMS.reticule("reticule",{},this.scene);
    		this.reticule.parent = this.camera;
    
    		const that = this;
    		const camera = that.camera ;

    		window.addEventListener("resize", ()=>{that.engine.resize();})
    		



    		setInterval(
        		()=>{   	
                		const ray = that.camera.getForwardRay();
    	        		const hit = that.scene.pickWithRay(ray);
                        //console.log(hit) ; 
    	        		if(hit.pickedMesh && hit.distance < 8){
    		        		that.reticule.material.emissiveColor = BABYLON.Color3.Green();

                    			console.log("??? > ",hit.pickedMesh.name) ; 
                    			let pickedActor = that.actorManager.getActor(hit.pickedMesh.name);
                    			if(pickedActor != null){
                        			this.focus = pickedActor ; 
                        			pickedActor.focus = true ; 
                        			//console.log(pickedActor) ; 
                    			}

    	        			} else {
    		        			that.reticule.material.emissiveColor = BABYLON.Color3.Red();
                    
                    				if(this.focus != null){
                        			this.focus.focus = false ;
                        			this.focus = null ; 
                    			}
                    
    	        		} 
            		},
        		10);

			setInterval(()=>{
				loadJSON("http://127.0.0.1:5000/tictac?Time="+this.clock, (res) => {});
			},
			10000);
	
	} // Fin du constructeur

    evalData(data){
        console.log("evalData") ; 
        console.log(data) ; 
        data.forEach((elt)=> {
            if(elt.op == "CREATE"){
                console.log("id = ", elt.id) ; 
                console.log("type = ",elt.type) ;
                elt.components.forEach((x) => {console.log(x.type);});
                console.log("===========================================================");
                const foo = ACTORS[elt.type] || ACTORS.actor ;
                const data = elt.components || []
                const actor = this.createActor(elt.id, foo, data) ; 

                elt.components.forEach((x) => {
                    console.log("type = ", x.type)
                    const foo = COMPS[x.type] ; 
                    const oPars = x.data ; 
                    const comp = new foo(oPars,actor) ; 
                })
            }
        })
    }


	
	createActor(name, TypeActor, data){
    		const actor = this.actorManager.createActor(name,TypeActor,data);
    		return actor;
	}
	
	removeActor(anActor){
		this.actorManager.removeActor(anActor) ; 
	}

    removeAllActors(){
        this.actorManager.removeAllActors();
    }

	getActor(name){
		return this.actorManager.getActor(name) ; 

	} 
	
	go(){
    		const that = this;
    		this.engine.runRenderLoop(()=>{
        		const dt = that.engine.getDeltaTime()/1000.0;
        		that.clock += dt ; 
        		that.update(dt) ; 
			that.actorManager.update(dt);
        		that.scene.render();
     		});
	}
	
	update(dt){}
	
	createWorld(){};
	
}

export {Simu} ; 


