
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


export {Position};
