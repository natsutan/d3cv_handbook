use image::{ImageBuffer, Rgb, RgbImage};
//use image::GenericImageView;
use image::GenericImage;
use image::DynamicImage;
use imageproc::drawing;

use imageproc::drawing::{Canvas, draw_filled_circle_mut};

pub struct PointImage {
    pub x: u32,
    pub y: u32
}

//fn circle(img: &mut RgbImage) {
//    draw_filled_circle_mut(img, (300, 300), 50, Rgb([0, 255, 0]));
//}

fn main() {
    let input_image_path = "data/chap2/mami1.png";
    let input_ori_image_path = "data/chap2/mami1_ori.png";
    let output_image_path = "result/chap2/mami1.png";



    let img = image::open(input_image_path).unwrap();
    println!("dimensions {:?}", img.dimensions());

    let size = img.dimensions();
    let width = size.0;
    let height = size.1;

    let mut feature_points = Vec::new();

    for y in 0..height-1 {
        for x in 0..width-1 {
            //rgb 186 147 110
            let rgb = img.get_pixel(x, y);
            let r_thresh:u8 = 170;
            let g_thresh:u8 = 110;
            let b_thresh:u8 = 110;
            if (rgb[0] > r_thresh) && (rgb[1] < g_thresh) && (rgb[2] < b_thresh) {
                feature_points.push(PointImage{x:x, y:y});
            }
        }
    }
    println!("points = {:?}", feature_points.len());



    let mut img_work = image::open(input_ori_image_path).unwrap().to_rgb8();

    let red  = Rgb([255,0,0]);


    for p in feature_points {
        let x:i32 = p.x.try_into().unwrap();
        let y:i32 = p.y.try_into().unwrap();

        draw_filled_circle_mut(&mut img_work, (x, y), 5, red);
    }

    match img_work.save(output_image_path) {
        Ok(_) => {
            println!("save to {:?}", output_image_path);
        }
        Err(e) => {
            println!("Error:{}", e);
        }
    }


}
