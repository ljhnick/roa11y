/**
 * initialization of variables
 *
 * @author Jiahao Li http://ljhnick.github.io
 */

// import * as THREE from '../lib/three.module.js';

var LEFTMOUSE = 1;
var MIDMOUSE = 2;
var RIGHTMOUSE = 3;

var WIDTHCONTAINER = 388;

var objects = new Array();

// colors
var BACKGROUNDCOLOR = 0xF2F0F0;
var GROUNDCOLOR = 0xF2F0F0;
var GRIDCOLOR = 0x888888;

var COLORNORMAL = 0xDB5B8A; // the normal color
var COLORCONTRAST = 0xD1D6E7; // is the contrast of the COLORNORMAL
var COLOROVERLAY = 0xF2F2F2; // 
var COLORHIGHLIGHT = 0xfffa90; //
var COLORSTROKE = 0xE82C0C;
var COLORYELLOW = 0xfffa90;


 // set up three js renderer
var renderer = new THREE.WebGLRenderer({
     antialias: true
});
renderer.setSize(window.innerWidth, window.innerHeight*0.5);
document.body.appendChild(renderer.domElement);

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 10000);
var gPosCam = new THREE.Vector3(-4, 6, 10);
camera.position.copy(gPosCam.clone().multiplyScalar(50));
var gLookAt = new THREE.Vector3(-25, 0, -0).multiplyScalar(10);
var gMouseCtrls = new THREE.TrackballControls(camera, undefined, gLookAt); // for mouse control

var cameraTop = new THREE.PerspectiveCamera(10, window.innerWidth / window.innerHeight, 1, 10000);
var cameraLeft = new THREE.PerspectiveCamera(10, window.innerWidth / window.innerHeight, 1, 10000);
// var cameraLeft = new THREE.OrthographicCamera(-200, 200, 200, -200, 1, 1000);

cameraTop.position.set(0, 2600, 0);
cameraTop.lookAt(new THREE.Vector3(0,0,0));
cameraLeft.position.set(-2600, 0, 0);
cameraLeft.lookAt(new THREE.Vector3(0,0,0));

//
// draw floor
//
function drawGround(yOffset) {
     var groundMaterial = new THREE.MeshBasicMaterial({
          color: GROUNDCOLOR,
          transparent: true,
          opacity: 0.5
     });


     var geometryGround = new THREE.CubeGeometry(1000, 1, 1000);
     var ground = new THREE.Mesh(
          geometryGround,
          groundMaterial,
          0 // mass
     );

     ground.position.y -= yOffset;
     return ground;
}
// var gGround = drawGround(0);
// scene.add(gGround);


// draw grid

function drawGrid(yOffset) {
     var gridHelper = new THREE.GridHelper( 1000, 40);
     gridHelper.position.y = yOffset;
     return gridHelper;
}
// var gGrid = drawGrid(0);
// scene.add(gGrid);

//
// add lights
//
var lights = [];
lights[0] = new THREE.PointLight(0xffffff, 1, 0);
lights[0].position.set(0, 100, -100);
// lights[0].castShadow = true;
scene.add(lights[0]);

/*
     initiate materials
*/
var MATERIALNORMAL = new THREE.MeshPhongMaterial({
     color: COLORNORMAL,
     transparent: true,
     opacity: 0.75
});


// for saving stl
var saveSTL = document.createElement( 'a' );
saveSTL.style.display = 'none';
document.body.appendChild( saveSTL );


// task type
var TASKTYPE;

var wheelDisabled = false;

