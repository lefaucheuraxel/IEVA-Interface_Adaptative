
import {Component} from './component.js' ; 


class Porte extends Component {

	constructor(data, actor){
	    super(data, actor) ; 
	    
	    const l = data.width  || 1.0 ; 
	    const h = data.height || 1.0 ; 
	    const e = data.depth  || 1.0 ; 
	    
	    const opts = {width:l, height:h, depth:e} ; 
	    const box = BABYLON.MeshBuilder.CreateBox(data.name,opts, actor.sim.scene) ; 
	    actor.object3d = box ; 
	    
	    box.isVisible       = false ; 
	    box.isPickable      = false ; 
	    box.checkCollisions = false ; 
	    

	}
}

export {Porte} ; 
