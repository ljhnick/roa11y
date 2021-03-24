var ROA11Y = ROA11Y || {};


renderer.setClearColor( BACKGROUNDCOLOR );
var render = function () {
	requestAnimationFrame( render );
	gMouseCtrls.update();
	// stats.update(); 

	// renderScene();

	// lights[0].position.copy(camera.position);
	renderer.render(scene, camera);
};

render();
renderer.domElement.hidden = true;
