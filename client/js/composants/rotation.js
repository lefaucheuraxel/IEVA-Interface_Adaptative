
import {PRIMS} from '../utils/prims.js' ; 
import {Component} from './component.js' ; 



class Rotation extends Component {

	constructor(data, actor){
		super(data, actor);
		
		const x = data.x || 0.0 ; 
        	const y = data.y || 0.0 ; 
        	const z = data.z || 0.0 ; 

        	if(this.actor.object3d != null){
        		console.log("ROTATION") ; 
	    		this.actor.rotation.set(x,y,z) ; 
            		this.actor.object3d.rotation = new BABYLON.Vector3(x,y,z) ; 
        	}
	}
}




export {Rotation};
