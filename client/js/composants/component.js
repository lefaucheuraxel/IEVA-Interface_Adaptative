
import {PRIMS} from '../utils/prims.js' ; 


class Component {
	
	constructor(data, actor){
		this.actor = actor;
	}
	
	register(dt){
		this.actor.components.push(this);
	}
	
	update(dt){}

    dispose(){}
}



export {Component};
