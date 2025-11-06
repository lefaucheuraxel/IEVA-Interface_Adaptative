
import {PRIMS} from '../utils/prims.js' ; 
import {Component} from './component.js' ; 


class Position extends Component {

	constructor(data, actor){
		super(data, actor);
        	const x = data.x || 0.0 ; 
        	const y = data.y || 0.0 ; 
        	const z = data.z || 0.0 ; 

        	if(this.actor.object3d != null){
	    		this.actor.position.set(x,y,z) ; 
            		this.actor.object3d.position.set(x,y,z) ; 
        	}
	}
}







class Box extends Component {

	constructor(data, actor){
		super(data, actor);
		const l = data.width    || 1.0 ;
		const h = data.height   || 1.0 ;
		const e = data.depth    || 1.0 ;   
        	const m = actor.sim.assets[data.material] || null ;  

        	const box = PRIMS.boite(data.name,{hauteur:h, largeur:l, epaisseur:e, 		materiau:m},this.actor.sim.scene) ; 
        	this.actor.object3d = box ; 
	}
}



export {Box};
