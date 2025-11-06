import {loadJSON} from './load.js' ; 
import {PRIMS} from './utils/prims.js';
import {ACTORS} from './entites/actor.js';
import {COMPS} from './composants/components.js';

import {Simu} from './simu.js' ; 

class Monde extends Simu {
  
  constructor(idCanvas){
    super(idCanvas) ; 
    this.prefixe = "./assets/expo/" ;
    
    this.assets = {} ; 
    
    const that = this ; 
    
    this.oldI = Math.floor((this.camera.position.x + 5)/10)
    this.oldJ = Math.floor((this.camera.position.z + 5)/10)
    
    window.addEventListener("click", (evt) => {
                  const that = this ; 
			      const ray = that.camera.getForwardRay();
			      const hit = that.scene.pickWithRay(ray);
			      if(hit.pickedMesh){
    				that.reticule.material.emissiveColor = BABYLON.Color3.Blue();
    				console.log("CLICK") ; 
    				console.log("!!! > ",hit.pickedMesh.name) ;
    				
    				if(hit.pickedMesh.name == "porteNord" || 
    				   hit.pickedMesh.name == "porteOuest" || 
    				   hit.pickedMesh.name == "porteSud" || 
    				   hit.pickedMesh.name == "porteEst"){
    				   
    				   
    				          console.log("SELECTION D UNE PORTE", hit.distance);
    				   	  const param = "http://127.0.0.1:5000/porte?Nom=" + hit.pickedMesh.name ; 
    				   	  loadJSON(param, (res) => {
					    		const data = JSON.parse(res) ; 

                                                        that.removeAllActors();
                                
                                                        const x = that.camera.position.x ; 
                                                        const z = that.camera.position.z ; 
                                                        that.camera.position.x = -x ; 
                                                        that.camera.position.z = -z ; 

                                                        that.camera.rotation.y = that.camera.rotation.y - Math.PI ; 

					    		that.evalData(data) ; 
					  	}) ;
					  
    				   }
    				else {
                    				console.log("XXX -> ", hit.pickedPoint) ; 
                    				const point = "&X="+hit.pickedPoint.x + "&Y=" + hit.pickedPoint.y + "&Z=" + hit.pickedPoint.z ; 
                    				console.log("Requête Point : ",point) ; 
    						const param = "http://127.0.0.1:5000/click?Nom=" + hit.pickedMesh.name + point ; 

						loadJSON(param, (res) => {
					    		const data = JSON.parse(res) ; 
					    		this.evalData(data) ; 
					  	}) ;

				
				//console.log("!!! > ",hit.pickedMesh.nom) ; 
			      	} 
    			        that.reticule.material.emissiveColor = BABYLON.Color3.Red();
			      }   
			    }); 
  }
  
  build(){
    
    const light1 = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(-10,10,-10), this.scene) ; 
    const light2 = new BABYLON.HemisphericLight("light2", new BABYLON.Vector3(-10,10,10), this.scene) ;
    const light3 = new BABYLON.HemisphericLight("light3", new BABYLON.Vector3( 10,10,-10), this.scene) ; 
    const light4 = new BABYLON.HemisphericLight("light4", new BABYLON.Vector3( 10,10,10), this.scene) ;
    //PRIMS.prairie("sol",{},this.scene);
    PRIMS.ciel("ciel",{},this.scene);	
    
    const materiau2 = PRIMS.materiauStandard("mat_sol",{texture:"./assets/textures/sol/parquet.jpg",uScale:125,vScale:125},this.scene);
    materiau2.specularColor = BABYLON.Color3.Black() ; 

    const materiau3 = PRIMS.materiauStandard("mat_sol",{texture:"./assets/textures/murs/dante.jpg",uScale:1,vScale:1},this.scene);
    materiau3.specularColor = BABYLON.Color3.Black() ; 		
    


    const sol = PRIMS.sol("sol", {materiau:materiau2}, this.scene) ;
    



    
    
    this.requete_assets() ; 
    this.requete_init();
  }
  
  
  update(dt){
  	const I = Math.floor((this.camera.position.x + 5)/10) ;   
  	const J = Math.floor((this.camera.position.z + 5)/10) ; 
  	
  	if(I != this.oldI || J != this.oldJ){
  	
  		console.log("Changement de salle - Position : ",I,' - ',J) ; 
  		this.oldI = I ; 
  		this.oldJ = J ; 
  		
  		this.requete_changement_de_salle() ;  
  	}
  }
  

   requete_changement_de_salle(){
   	const requete = "http://127.0.0.1:5000/salle?I="+this.oldI+"&J="+this.oldJ ; 
   	loadJSON(requete, (res) => {
	       const data = JSON.parse(res) ; 
	       
	       console.log("DATA JSON = ",data) ; 
	       
	       this.evalData(data) ;    	
   	}) ; 
   }
  
  requete_tous(){
    
    loadJSON("http://127.0.0.1:5000/",(res) => {
	       console.log(">>??", res) ;
	       
	       (JSON.parse(res)).forEach(element => {
					   
					   const x = (0.5-Math.random())*50 ; 
					   const y = 3 ; 
					   const z = 50*Math.random() ;
					   const poster = this.createActor(element,ACTORS.actor,{})
					     .add(COMPS.poster,{nom: element, largeur:5, hauteur:3, tableau: this.prefixe+element+".jpg"})
					     //.add(COMPS.cartel,{titre:element})
					     .add(COMPS.position,{x,y,z});
					   
					   
					 });
	     })
      }

  requete_assets(){
  	loadJSON("http://127.0.0.1:5000/assets", (res) => {
  		const data = JSON.parse(res) ; 
  		console.log(data) ; 
  		for(const cle in data){
  			console.log(">>>>>>>>>>>>>>>  ", cle) ; 
  			const spec    = data[cle] ; 
  			const rvb = spec.color || [0,0,0] ; 
  			const couleur = new BABYLON.Color3(rvb[0], rvb[1], rvb[2]);
  			const texture = spec.texture || null ; 
  			const uScale  = spec.uScale  || 1.0 ;
  			const vScale  = spec.vScale  || 1.0 ;  
  			
  			var materiau = null ; 
  			
  			if(texture != null){
  				materiau =  PRIMS.materiauStandard(
  				                 cle,
  				                 {couleur:couleur,texture:texture,uScale,vScale},
  				                 this.scene) ; 
  			} else {
  			        materiau =  PRIMS.materiauStandard(cle,{couleur:couleur},this.scene) ;
  			}
  			
  			this.assets[cle] = materiau ; 
  		}

  	});  	
  }
  
  requete_init(){
    loadJSON("http://127.0.0.1:5000/init",(res) => {
	       console.log(">>??", res) ;
	       
	       const data = JSON.parse(res) ; 
	       
	       console.log("DATA JSON = ",data) ; 
	       
	       this.evalData(data) ; 
	       
        })
      }
  
}
  
  export {Monde} ; 



