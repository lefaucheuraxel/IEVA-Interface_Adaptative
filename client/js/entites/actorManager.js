
import {SafeArray} from '../utils/safeArray.js';


class ActorManager {

    constructor(data, sim) {
        this.sim = sim ; 
        this.actors = new SafeArray();
    }
    
    createActor(name,TypeActor,data) {
        const actor = new TypeActor(name,data,this.sim);
        this.actors.add(actor);
        return actor;
    }
    
    add(actor){
    	this.actors.add(actor);
    	return actor;
    }
    
    
    
    removeActor(actor) {
        this.actors.remove(actor);
        actor.dispose() ; 
        //actor.removeAll();
    }
    
    getActor(name) {
        let aux = null;
        this.actors.forEach(actor => {
            if (actor.name == name) {
                aux = actor;
            }
        })
        return aux
    }
    
    removeAllActors() {
        this.actors.forEach((actor) => {this.removeActor(actor);})
    }
    
    removeActorByName(name){
        this.actors.forEach(actor => {
            if (actor.name == name) {
                this.removeActor(actor)
            }
        })
    }
    
    update(dt) { //dt
    	// console.log("================================ date : ", this.sim.clock); 
    	//console.log(this.actors) ; 
    	this.actors.forEach(actor => {actor.executeComponents(dt);});
        this.actors.forEach(actor => {	//console.log(actor.name, " ", actor.position) ; 
        				actor.update(dt)}
        			      );
    }
}

export {ActorManager} ; 
