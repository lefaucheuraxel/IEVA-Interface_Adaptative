
import {PRIMS} from '../utils/prims.js' ; 
import {Component} from './component.js' ; 








class Wall extends Component {

	constructor(data, actor){
		super(data, actor);
		const l = data.width  || 1.0 ;
		const h = data.height || 1.0 ;
		const e = data.depth  || 1.0 ;    
		const m = actor.sim.assets[data.material] || null ;
        	const wall = PRIMS.cloison(data.name,{hauteur:h, largeur:l, epaisseur:e,"materiau":m},this.actor.sim.scene) ; 
        	this.actor.object3d = wall ; 
	}
}













export {Wall};
