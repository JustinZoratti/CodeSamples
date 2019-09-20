/*
draws 'global.darkness_ring_count' concentric rings of thickness 'global.darkness_ring_thickness' and decreasing
opacity at each of the light_source instances in the current room
*/

//create surfaces to store the lighting overlays
//each surface represents a layer of darkness with uniform opacity
for(var i = 0; i < global.darkness_ring_count; i++)
{
	if(!surface_exists(shadows[i]))
	{
		shadows[i] = surface_create(global.rw, global.rh)
	}
}

//clear shadows[0] to solid black
//shadows[0] represents the region of darkness outside all light_sources
surface_set_target(shadows[0])
draw_clear_alpha(c_black,1)
surface_reset_target()

//clear the other surfaces in 'shadows' to transparency
for(var i = 1; i < global.darkness_ring_count; i++)
{
	surface_set_target(shadows[i])
	draw_clear_alpha(c_black,0)
	surface_reset_target()
}

//draw black circles on each surface in 'shadows' except shadows[0]
global.d_radius = 0
draw_set_color(c_black)
for(var i = 1; i < global.darkness_ring_count; i++)
{
	surface_set_target(shadows[i])
	with(light_source) //draw a black circle of radius 'r + d_radius' at each light_source
	{
		event_perform(ev_draw,0)
	}
	surface_reset_target()
	
	global.d_radius -= global.darkness_ring_thickness //decrease the radius of the circles
}

//erase the center of each of the black circles from the previous loop to create rings
//operates on all 'shadows', including shadows[0]
global.d_radius = 0
gpu_set_blendmode(bm_subtract)
draw_set_color(c_white)
for(var i = 0; i < global.darkness_ring_count; i++)
{
	surface_set_target(shadows[i])
	with(light_source) //erase a circle of radius 'r + d_radius' at each light_source
	{
		event_perform(ev_draw,0)
	}
	surface_reset_target()
	
	global.d_radius -= global.darkness_ring_thickness
}
gpu_set_blendmode(bm_normal)

//draw the surfaces to the screen
draw_set_alpha(1) //start at max opacity
for(var i = 0; i < global.darkness_ring_count; i++)
{
	//draw the surface with opacity scaled by the global darkness maximum
	draw_surface_ext(shadows[i], global.vx, global.vy, 1, 1, 0, c_white, global.max_darkness*draw_get_alpha())
	
	//decrease the drawing opacity linearly
	draw_set_alpha(draw_get_alpha() - 1/global.darkness_ring_count)
}