
import {PRIMS} from '../utils/prims.js' ; 
import {Component} from './component.js' ; 







class Sphere extends Component {

	constructor(data, actor){
		super(data, actor);
		const diametre = data.diameter || 1.0 ;  
		const m = actor.sim.assets[data.material] || null ;
        	const sph = PRIMS.sphere(data.name,{diametre:diametre, materiau:m},this.actor.sim.scene) ; 
        	this.actor.object3d = sph ; 
	}
}



export {Sphere};
