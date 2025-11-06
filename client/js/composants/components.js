
import {PRIMS} from '../utils/prims.js' ; 

import {Component}  from './component.js' ;
import {AnchoredTo} from './anchoredTo.js' ; 
import {Position}   from './position.js' ;
import {Rotation}   from './rotation.js' ; 
import {Poster}     from './poster.js' ; 
import {Sphere}     from './sphere.js' ; 
import {Box}        from './box.js' ; 
import {Wall}       from './wall.js' ; 
import {Porte}      from './porte.js' ;

class Cartel extends Component {

	constructor(data, actor){
		super(data, actor);

        this.register(300);

        this.sim = actor.sim ; 

        this.titre = data.titre || "" ; 
        this.descript = data.descript || "" ; 
        this.timer = 0;
        this.setUp = false ; 
        this.visible = false ; 

        this.rect = new BABYLON.GUI.Rectangle ; 
        this.rect.adaptWidthToChildren = true ; 
        this.rect.adaptHeightToChildren = true ;
        this.rect.paddingLeft  = "-10px";
        this.rect.paddingRight = "-10px";
        this.rect.height = "40px";
        this.rect.cornerRadius = 40 ; 
        this.rect.background = "green" ; 
        this.rect.alpha = 0 ;
        this.rect.linkOffsetY = 100 ; 
        this.actor.sim.gui.addControl(this.rect) ; 
        //const gui = BABYLON.GUI.AdvancedDynamicTexture.CreateForMesh(this.actor.object3d,200,250,false) ; 
        //gui.addControl(this.rect) ;

        this.label = new BABYLON.GUI.TextBlock() ; 
        this.label.text = this.titre ; 
        this.label.resizeToFit = true ;
        this.label.color = "black" ;
        this.label.alpha = 0 ; 
        this.rect.addControl(this.label) ; 

        this.gui_affiche = false ; 
        this.gui_description = false ; 
       
	}

    update(dt){
        //console.log("UPDATE");
        if(this.setUp == false){
            this.rect.linkWithMesh(this.actor.object3d);
            this.setUp = true ; 
            console.log(this.actor.name + "-OUPS") ; 
        }

        if(this.actor.focus){
            this.rect.alpha = 1 ; 
            this.label.alpha = 1
        } else {
            this.rect.alpha = 0 ; 
            this.label.alpha = 0 ; 
        }
    }
}


class Titre extends Component {

	constructor(data, actor){
		super(data, actor);


        this.register();

        this.sim = actor.sim ; 

        const scene = this.sim.scene ;
        const nom = data.titre ; 

        this.plane = BABYLON.Mesh.CreatePlane("plane-"+nom);
        if(actor.object3d){this.plane.parent = actor.object3d;}
        plane.position.y = -0.1 ; 
        plane.visibility = 0 ;
        plane.isPickable = false ; 
        const header = BABYLON.GUI.Button.CreateSimpleButton(nom, nom) ; 
        header.width = "200px" ; 
        header.height = "40px" ;
        header.color  = "black" ; 
        header.fontSize = 18 ;
        header.background = "white" ; 
        header.isVisible = true ; 
        this.sim.gui.addControl(header) ; 
        header.linkWithMesh(plane) ; 
        
    

    }

}



class LookAt extends Component {

	constructor(data, actor){
		super(data, actor);
		this.register() ; 
	}

    update(dt){
        this.actor.object3d.lookAt(this.actor.sim.camera.position) ; 
    }
}


class Repulsion extends Component {

	constructor(data, actor){
		super(data, actor) ; 
		this.register() ; 
		this.f = new BABYLON.Vector3(0,0,0) ;
		this.A = new BABYLON.Vector3(0,0,0) ; // Position de ce vecteur
		this.B = new BABYLON.Vector3(0,0,0) ;
	}
	
	update(dt){
		this.A.copyFrom(this.actor.position) ; 
		this.actor.sim.actorManager.actors.forEach((b)=>{
			this.B.copyFrom(b.position) ; 
			this.B.subtractToRef(this.A, this.f) ;
			const d = this.f.length() ; 
			if(d<10){
				this.f.normalize() ; 
				this.f.scaleInPlace(-1) ; 
				this.f.y = 0 ; 
				this.actor.applyForce(this.f) ;
			} 
		}) ; 
	
	}
}

class Frottement extends Component {

	constructor(data, actor){
		super(data, actor) ; 
		this.register() ; 
		this.f = new BABYLON.Vector3(0,0,0) ; 
		this.k = data.k || 0.5 ; 
	}
	
	update(dt){
		this.f.copyFrom(this.actor.velocity) ; 
		this.f.scaleInPlace(-this.k) ;
		this.actor.applyForce(this.f) ;  	
	}
}

class Attraction extends Component {

	// data : 
	//	d0 			type : float, default : 1.0, 	distance between the attractor and the target point
	//	attractorName 		type : string, default : null	name of the attractor actor 

	constructor (data, actor){
		super(data, actor) ; 
		this.register() ;
		
		console.log("CREATION ATTRACTEUR") ; 
		
		const attractorName = data.attractedBy || null ; 
		
		this.target 	= new BABYLON.Vector3(0,0,0) ; 
		this.maPosition = this.actor.position.clone() ; 
		
		this.d0 = data.d0 || 1.0 ; 
		
		this.vd = new BABYLON.Vector3(0,0,0) ;  // Desired velocity
		
		this.force = new BABYLON.Vector3(0,0,0) ; 
		
		 
		if(attractorName){
			this.attractor = actor.sim.actorManager.getActor(attractorName) || null ; 			
		}		 
	}
	
	update(dt){

		if(this.attractor){
			// Calcul du point cible 

			this.force.copyFrom(this.attractor.position) ; 
			this.force.subtractInPlace(this.actor.position) ; 
			
			const d = this.force.length() ; 
			
			if(d > 1){
				this.force.normalize() ; 
			}
			
			this.actor.applyForce(this.force) ; 
			
		}	
		
	
	}
}



const COMPS = {
    porte      : Porte, 
	anchoredTo : AnchoredTo,
    	titre      :  Titre,
    	cartel     :  Cartel, 
	position   : Position,
	rotation   : Rotation,
	poster     : Poster,
	sphere     : Sphere, 
	box        : Box,
	wall       : Wall,
	lookAt 	   : LookAt,
	frottement : Frottement, 
	repulsion  : Repulsion, 
    	attraction : Attraction,
	component  : Component
};

export {COMPS};
