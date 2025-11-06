

function creerScene(){
	let scn = new BABYLON.Scene(engine) ; 
	scn.gravity = new BABYLON.Vector3(0,-9.8,0) ; 
	scn.collisionsEnabled = true ;
	return scn ;
}


// function creerCamera(name,data,scene){
function creerCamera(name,options,scn){	
	// console.log("creation camera");
	// Création de la caméra
	// =====================
	
    const canvas = scn.getEngine().getRenderingCanvas() ;
	const camera = new BABYLON.UniversalCamera("camera", new BABYLON.Vector3(10,1.7,12), scn) ; 
	//camera = new BABYLON.UniversalCamera(name,new BABYLON.Vector3(10,1.7,5),scn) ;
	camera.setTarget(new BABYLON.Vector3(10.0,0.7,10.0)) ; 

	camera.checkCollisions = true ;
	camera.ellipsoid = new BABYLON.Vector3(0.5,1.0,0.5) ;
	camera.applyGravity = true ;
	camera.keysUp = [90,38];
	camera.keysDown = [40,83];
	camera.keysLeft = [81,37];
	camera.keysRight = [68,39];
	camera.attachControl(canvas) ;
	camera.inertia = 0.01;
	camera.angularSensibility  = 1000;
	camera.minZ = 0.1;
	
	camera.fov = 1.22 ; // 70 degrés

	camera.attachControl(canvas, false) ; 


	return camera
	
}

function creerSol(name,options,scn){
	options = options || {} ; 
	const taille   = options.taille   || 500.0 ; 
	let materiau = options.materiau || null ;
	
	const sol = BABYLON.Mesh.CreateGround(name,taille,taille,2.0,scn) ;
	
	if(materiau){
		sol.material = materiau ; 
	} else {
		materiau = new BABYLON.StandardMaterial("materiau-defaut-" + name, scn) ; 
		materiau.diffuseColor = new BABYLON.Color3(1.0,0.0,0.0) ;   
		sol.material = materiau ; 
	}
	
    sol.checkCollisions = true ;
	
	return sol ; 
	
}

function creerPrairie(name,options,scn){
    const pickable = options.pickable || false;
	let sol = BABYLON.Mesh.CreateGround(name,220.0,220.0,2.0,scn) ;
	sol.checkCollisions = true ;
    sol.isPickable = pickable;
	sol.material = new BABYLON.StandardMaterial("blanc",scn) ;
	// sol.material.diffuseColor  = new BABYLON.Color3(1.0,0,0) ;
	sol.material.diffuseTexture = new BABYLON.Texture('./assets/textures/grass.png',scn);
	sol.material.specularTexture = new BABYLON.Texture('./assets/textures/grass.png',scn);
	sol.material.emissiveTexture = new BABYLON.Texture('./assets/textures/grass.png',scn);
	sol.material.ambientTexture = new BABYLON.Texture('./assets/textures/grass.png',scn);
	sol.material.diffuseTexture.uScale = 10.0;
	sol.material.diffuseTexture.vScale = 10.0;
	sol.material.specularTexture.uScale = 10.0;
	sol.material.specularTexture.vScale = 10.0;
	sol.material.emissiveTexture.uScale = 10.0;
	sol.material.emissiveTexture.vScale = 10.0;
	sol.material.ambientTexture.uScale = 10.0;
	sol.material.ambientTexture.vScale = 10.0;
	sol.receiveShadows = true;
	sol.metadata = {"type": 'ground'}
	return sol
}

function creerMateriauStandard(nom,options,scn){
	let couleur = options.couleur || null ; 
	let texture = options.texture || null ; 
	let uScale  = options.uScale  || 1.0 ; 
	let vScale  = options.vScale  || 1.0 ; 

	let materiau = new BABYLON.StandardMaterial(nom,scn) ; 
	if(couleur != null) materiau.diffuseColor = couleur ; 
	materiau.specularColor = BABYLON.Color3.Black() ; 
	if(texture!= null){
		materiau.diffuseTexture = new BABYLON.Texture(texture,scn) ; 
		materiau.diffuseTexture.uScale = uScale ; 
		materiau.diffuseTexture.vScale = vScale ; 
	}
	return materiau ; 
}



function creerSphere(nom,opts,scn){

	let options  = opts || {} ; 
	let diametre = opts.diametre || 1.0 ; 
	let materiau = opts.materiau || null ; 
	
	if(materiau == null){
		materiau = new BABYLON.StandardMaterial("blanc",scn) ;
		materiau.diffuseColor = new BABYLON.Color3(1.0,1.0,1.0) ; 
	}

	let sph = BABYLON.Mesh.CreateSphere(nom,16,diametre,scn) ;
	sph.material              = materiau

	return sph;

}

function creerCylindre(nom,opts,scn){
	let options  = opts || {} ; 
	let diametre = opts.diametre || 1.0 ; 
	let hauteur = opts.hauteur || 1.0 ;
	let materiau = opts.materiau || null ; 
	
	if(materiau == null){
		materiau = new BABYLON.StandardMaterial("blanc",scn) ;
		materiau.diffuseColor = new BABYLON.Color3(1.0,1.0,1.0) ; 
	}

	let cyl = BABYLON.MeshBuilder.CreateCylinder(nom,{height:hauteur,diameter:diametre},scn) ;
	cyl.material              = materiau

	return cyl;
}

function creerPoster(nom,opts,scn){

	let options = opts || {} ; 
	let hauteur = options["hauteur"] || 1.0 ; 
	let largeur = options["largeur"] || 1.0 ; 	
	let textureName = options["tableau"] || ""; 

	console.log("@ ", nom) ; 
	let tableau1 = BABYLON.MeshBuilder.CreatePlane(nom, {width:largeur,height:hauteur}, scn);
    	tableau1.name = nom ; 
	let verso = BABYLON.MeshBuilder.CreatePlane("verso-" + nom, {width:largeur,height:hauteur}, scn);

    
   	verso.z = 0.05 ; 
    	verso.rotation.y = Math.PI ;
    	verso.parent = tableau1 ; 
    
    	const col = new BABYLON.Color3(1,1,1) ; 
    	const mat = creerMateriauStandard("mat-"+nom,{couleur:col,texture:textureName},scn)


	tableau1.material = mat;

	tableau1.checkCollisions = true;
    	tableau1.isPickable = true ;

    	verso.checkCollisions = true ; 
    	verso.isPickable = false ; 

    	return tableau1 ; 
}

function creerCloison(nom,opts,scn){
	
	let options   = opts || {} ; 
	let hauteur   = options.hauteur || 3.0 ; 
	let largeur   = options.largeur || 5.0 ; 
	let epaisseur = options.epaisseur || 0.1 ;

	let materiau   = options.materiau || new BABYLON.StandardMaterial("materiau-pos"+nom,scn); 
	
	console.log(">> ", nom, " ==> ", materiau) ; 

    	let groupe = new BABYLON.TransformNode("groupe-"+nom) ; 

	let cloison = BABYLON.MeshBuilder.CreateBox(nom,{width:largeur,height:hauteur,depth:epaisseur},scn) ;
	cloison.name       = nom ; 
	cloison.material   = materiau ; 
	cloison.parent     = groupe ; 
	cloison.position.y = hauteur / 2.0 ; 

    	cloison.checkCollisions = true ;

    return groupe ;  
}

//--Ajouts Personels--
function creerPlafond(nom,opts,scn){
   let options   = opts || {} ; 
   let height   = options.height || 10.0 ; 
   let longueur   = options.longueur || 30.0 ; 
   let largeur   = options.largeur || 30.0 ; 
   let position_x = options.position_x || largeur / 2.0 - 15.0 ;
   let position_z = options.position_z || 0.0 ;

   let materiau   = options.materiau || new BABYLON.StandardMaterial("materiau_plafond-pos"+nom,scn); 

	   let groupe = new BABYLON.TransformNode("groupe-"+nom) ; 

   let plafond = BABYLON.MeshBuilder.CreatePlane("plafond-" + nom, {width:largeur,height:longueur}, scn);
   plafond.material = materiau ; 
   plafond.parent = groupe ; 
   plafond.position.x = position_x; 
   plafond.position.y = height; 
   plafond.position.z = position_z; 

   plafond.rotation.x = -Math.PI/2 ; 

   plafond.checkCollisions = false ;

   return groupe ;  
}





function creerCiel(nom,options,scene){
    const pickable = options.isPickable || false ; 
    const skyMaterial = new BABYLON.StandardMaterial("mat_skybox", scene);
    skyMaterial.backFaceCulling = false ;
    skyMaterial.reflectionTexture = new BABYLON.CubeTexture("./assets/skybox/skybox", scene);
    skyMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
    skyMaterial.diffuseColor = new BABYLON.Color3(0,0,0);
    skyMaterial.specularColor = new BABYLON.Color3(0,0,0);

    const skyBox = BABYLON.Mesh.CreateBox("skybox",100,scene);
    skyBox.material = skyMaterial ;

    skyBox.isPickable = pickable ;

    return skyBox ;
}

function creerAmer(nom,opts,scn){
	let options  = opts             || {}   ; 
	let taille   = options.taille   || 1.0  ; 
	let pos_x    = options.pos_x   || 0.0  ; 
	let pos_y    = options.pos_y   || 1.0  ; 
	let pos_z    = options.pos_z   || 0.0  ; 

	let materiau = new BABYLON.StandardMaterial("materiau-amer-"+nom,scn); 

	materiau.alpha = 0.4;

    	let groupe = new BABYLON.TransformNode("groupe-"+nom) ; 

	let amer = BABYLON.MeshBuilder.CreateSphere(nom,{diameter:taille},scn) ;
	
	amer.name = nom ; 

	amer.material = materiau ; 
	amer.parent = groupe ; 
	amer.position.x = pos_x;
	amer.position.y = pos_y;
	amer.position.z = pos_z;

	amer.checkCollisions = false ;

    return groupe ;  
}

function creerBoite(nom,opts,scn){
	let options   = opts || {} ; 
	let hauteur   = options.hauteur || 2 ; 
	let largeur   = options.largeur || 5.0 ; 
	let epaisseur = options.epaisseur || 0.1 ;

	let materiau   = options.materiau || new BABYLON.StandardMaterial("materiau-pos"+nom,scn); 

	let cloison = BABYLON.MeshBuilder.CreateBox(nom,{width:largeur,height:hauteur,depth:epaisseur},scn) ;
	cloison.name     = nom ; 
	cloison.material = materiau ; 
	//cloison.parent = groupe ; 
	cloison.position.y = hauteur / 2.0 ; 
	cloison.checkCollisions = true ;

    return cloison ;  
}

function creerReticule(nom, opts, scn){
	const reticule = BABYLON.MeshBuilder.CreateSphere("reticule", {segments:4, diameter:0.0025}, scn);
	const retMat   = new BABYLON.StandardMaterial("reticuleMat", scn);
	retMat.emissiveColor = BABYLON.Color3.Red();
	retMat.specularColor = BABYLON.Color3.Black();
    retMat.diffuseColor  = BABYLON.Color3.Black();
	reticule.material = retMat ; 
	reticule.isPickable = false;
	reticule.position.z = 0.3;  
	
	return reticule;
}

function creerTitre(name, data, scene){

    const parent = data.parent || null ; 
    const text   = data.texte  || "" ; 

	var textTexture = new BABYLON.DynamicTexture(name, { width: 512, height: 256 }, scene, true);

	// Create a transparent material for the text plane
	var textMaterial = new BABYLON.StandardMaterial("textMaterial"+name, scene);
	textMaterial.diffuseTexture = textTexture;
	textMaterial.opacityTexture = textTexture; // Use the texture for opacity
	textMaterial.alpha = 0.99; // Set alpha slightly below 1 to enable transparency
	
	var textPlaneF = BABYLON.Mesh.CreatePlane("textPlane"+name, 5, scene);
	textPlaneF.material = textMaterial;
	textPlaneF.scaling.x = 1;
    //textPlaneF.rotation.y = Math.PI;
	textPlaneF.position = new BABYLON.Vector3(0.0, 0.35, 0.0);
	if (parent != null) textPlaneF.parent = parent; // Set the parent of the text plane to the new mesh
	
	var textContext = textTexture.getContext();
	textContext.clearRect(0, 0, textTexture.getSize().width, textTexture.getSize().height);
	
	textContext.font = "17px Arial";
	textContext.fillStyle = "red";
	textContext.fillText(text, 20, 80);
	
	textTexture.update();

	textPlaneF.isVisible = false;
    textPlaneF.isPickable = false;

	return textPlaneF;
};

function creerDescription(name, data, scene){

    const parent = data.parent || null ; 
    const desc   = data.texte || "" ; 

	var textTexture = new BABYLON.DynamicTexture(name, { width: 512, height: 256 }, scene, true);

	// Create a transparent material for the text plane
	var textMaterial = new BABYLON.StandardMaterial("textMaterial", scene);
	textMaterial.diffuseTexture = textTexture;
	textMaterial.opacityTexture = textTexture; // Use the texture for opacity
	textMaterial.alpha = 0.99; // Set alpha slightly below 1 to enable transparency
	
	var textPlaneF = BABYLON.Mesh.CreatePlane("textPlane", 5, scene);
	textPlaneF.material = textMaterial;
	textPlaneF.scaling.x = -1;
	textPlaneF.position = new BABYLON.Vector3(-1.05, -2.35, -0.01);
	if(parent != null)textPlaneF.parent = parent; // Set the parent of the text plane to the new mesh
	
	var textContext = textTexture.getContext();
	textContext.clearRect(0, 0, textTexture.getSize().width, textTexture.getSize().height);
	
	textContext.font = "11px Arial";
	textContext.fillStyle = "white";


	if (desc.length > 43){
		textContext.fillText("Description: "+desc.substring(0,43), 20, 100);
		let lines = Math.ceil((desc.length - 43)/ 55);
		for (let i = 0; i < lines; i++) {
			if (i<lines-1){
				textContext.fillText(desc.substring(43+55*i,43+55*(i+1)), 20, 110+10*i);
			} else {
				textContext.fillText(desc.substring(43+55*i), 20, 110+10*i);
			}
			
		}
	} else {
		textContext.fillText("Description: "+desc, 20, 100);
	}
	
	textTexture.update();

	textPlaneF.isVisible = false;

	return textPlaneF;
};

function creuser(mesh0, mesh1){
    const csg0 = BABYLON.CSG.FromMesh(mesh0);
    const csg1 = BABYLON.CSG.FromMesh(mesh1) ; 
    csg0.subtractInPlace(csg1);
    const csgMesh = csg0.toMesh() ;
    mesh0.dispose() ; 
    mesh1.dispose() ; 
    return csgMesh ;  
}


const PRIMS = {
"camera":creerCamera,
"cloison":creerCloison,
"sphere":creerSphere,
"cylindre":creerCylindre,
"poster":creerPoster,
"materiauStandard":creerMateriauStandard,
"prairie":creerPrairie,
"sol":creerSol,
"ciel":creerCiel,
"amer":creerAmer,
"reticule":creerReticule,
"boite":creerBoite,
"titre":creerTitre,
"description":creerDescription,
"creuser":creuser
}

export {PRIMS} ; 
