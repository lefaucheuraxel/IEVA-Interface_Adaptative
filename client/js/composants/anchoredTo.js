
import {PRIMS} from '../utils/prims.js' ; 
import {Component} from './component.js' ; 


class AnchoredTo extends Component {

	constructor(data, actor){
		super(data, actor) ;
		const nomParent = data.parent || null ;
		
		if(nomParent != null){
		
			const parent = actor.sim.getActor(nomParent) ; 
			
			if(parent != null){
				if(actor.object3d && parent.object3d){
					actor.object3d.parent = parent.object3d ; 
				}
			}
		}
	
	}

}



export {AnchoredTo};
