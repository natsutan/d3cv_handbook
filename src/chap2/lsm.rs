use image::{DynamicImage, GenericImageView};

pub struct PointImage {
    pub x: u32,
    pub y: u32
}

fn main() {
    let input_image_path = "data/chap2/mami1.png";

    println!("Hello, world!");

    let img = image::open(input_image_path).unwrap();
    println!("dimensions {:?}", img.dimensions());

    let size = img.dimensions();
    let width = size.0;
    let height = size.1;
 /*   for y in 0..height-1 {
        for x in 0..width-1 {
            //rgb 186 147 110
            let rgb = img.get_pixel(x, y);
            let r_thresh:u8 = 150;
            let g_thresh:u8 = 150;
            let b_thresh:u8 = 150;
            if rgb.0[0] > r_thresh && rgb.0[1] < g_thresh && rgb.0[2] < b_thresh {
                println!("{:?}, {:?}", x, y);
            }
        }
    }*/


}
