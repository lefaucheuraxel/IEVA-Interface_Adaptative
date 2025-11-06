
//import {COMPS} from '../composants/components.js' ; 

function removeArrayElement(array, element) {
    const ndx = array.indexOf(element);
    if (ndx >= 0) {
        array.splice(ndx, 1);
    }
}


class Actor {
    constructor(name, data, sim) {
        this.name       = name;
        this.components = []; 
        this.sim        = sim ;  
        this.object3d   = null ; 
        this.focus      = false ; 
        this.position   = new BABYLON.Vector3(0.0,0.0,0.0) ; 
        this.rotation   = new BABYLON.Vector3(0.0,0.0,0.0) ; 
        this.direction  = new BABYLON.Vector3(0.0,0.0,-1.0) ;
    }
    
    addComponent(component) {
        //this.components.push(component);
        return this;
    }
    
    add(ComponentType, data) {
    	data.name = this.name ; 
        const component = new ComponentType(data, this);
        // this.components.push(component);
        return this;
    }
    
    removeComponent(component) {
        removeArrayElement(this.components, component);
    }
    

    getComponent(ComponentType) {
        return this.components.find(c => c instanceof ComponentType);
    }
    
    executeComponents(dt) {
        //console.log("Exécution des composants de : ", this.name);
        //console.log(this.components) ; 
        this.components.forEach((c)=>{c.update(dt);})
    }
    
    update(dt){}

    dispose(){
        if(this.object3d){
            this.object3d.dispose() ; 
        }
    }
}

class ActorDyn extends Actor {

	constructor(name, data, sim){
		super(name, data, sim);
		this.mass     = data.mass || 1.0 ; 
		this.velocity = new BABYLON.Vector3(0,0,0) ; 
		this.force    = new BABYLON.Vector3(0,0,0) ; 
	}

	applyForce(f){
		this.force.addInPlace(f) ; 
	}

	update(dt){
	
		//console.log("=> ", this.name, " : ", this.force) ; 
		//console.log("Acteur : ", this.sim.clock);
		this.velocity.scaleAndAddToRef(dt,this.position) ; 
		this.force.scaleAndAddToRef(dt/this.mass, this.velocity) ; 
		this.force.set(0,0,0) ; 

		if(this.object3d){
			this.object3d.position.copyFrom(this.position) ; 
		}

	}
}

class Poster extends Actor {

    constructor(name, data, sim){
        super(name, data, sim) ;

    }

}

const ACTORS = {
        poster : Poster,
	    actorDyn : ActorDyn,
        actor : Actor
}

export {ACTORS};

