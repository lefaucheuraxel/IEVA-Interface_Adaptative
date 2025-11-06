import {Component} from './component.js' ; 
import {PRIMS} from '../utils/prims.js' ; 



class Poster extends Component {

	constructor(data, actor){
		super(data, actor);
		console.log("@@ ",data.name) ; 
        	const poster = PRIMS.poster(data.name, data, this.actor.sim.scene);
        	this.actor.object3d = poster;
	}
}



export {Poster};
