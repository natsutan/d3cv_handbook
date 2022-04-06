use std::cmp;
use image::{DynamicImage, GenericImageView, Rgb, RgbImage};
use imageproc::drawing::draw_filled_circle_mut;

pub struct PointImage {
    pub x: u32,
    pub y: u32
}

pub struct PointLogical {
    pub x: f32,
    pub y: f32
}

pub fn find_features(img: &DynamicImage) -> Vec<PointImage> {
    let mut feature_points = Vec::new();

    let size = img.dimensions();
    let width = size.0;
    let height = size.1;

    for y in 0..height-1 {
        for x in 0..width-1 {
            let rgb = img.get_pixel(x, y);
            let r_thresh:u8 = 170;
            let g_thresh:u8 = 110;
            let b_thresh:u8 = 110;
            if (rgb[0] > r_thresh) && (rgb[1] < g_thresh) && (rgb[2] < b_thresh) {
                feature_points.push(PointImage{x:x, y:y});
            }
        }
    }

    feature_points
}

pub fn plot_feature_point(img_bg: &mut RgbImage, points:Vec<PointImage> ,col: Rgb<u8>, output_image_path: &str) {
    for p in points {
        let x:i32 = p.x.try_into().unwrap();
        let y:i32 = p.y.try_into().unwrap();

        draw_filled_circle_mut( img_bg, (x, y), 5, col);
    }

    match img_bg.save(output_image_path) {
        Ok(_) => {
            println!("save to {:?}", output_image_path);
        }
        Err(e) => {
            println!("Error:{}", e);
        }
    }
}

pub fn get_f0(img: &DynamicImage) -> u32 {
    let size = img.dimensions();
    cmp::max(size.0, size.1)
}

pub fn im_to_log(src: &PointImage, f0: &u32) -> PointLogical {
    let fi = (f0 / 2) as i32;
    let xi = src.x as i32;
    let yi = src.y as i32;

    let x = (xi - fi) as f32;
    let y = (yi - fi) as f32;
    PointLogical{x, y}
}

pub fn log_to_im(src: &PointLogical, f0: &u32) -> PointImage {
    let fi = *f0 as i32;
    let xi = src.x as i32 + (fi / 2);
    let yi = src.y as i32 + (fi / 2);

    let xu :u32 = cmp::max(xi, 0) as u32;
    let yu :u32 = cmp::max(yi, 0) as u32;

    PointImage{x:xu, y:yu}
}

pub fn eta_from_xyf(p:&PointLogical, f0: &u32) -> [f32;6] {
    let mut eta = [0.0;6];
    let f:f32 = *f0 as f32;

    eta[0] = p.x * p.x;
    eta[1] = 2.0 * p.x * p.y;
    eta[2] = p.y * p.y;
    eta[3] = 2.0 * f * p.x;
    eta[4] = 2.0 * f * p.y;
    eta[5] = f * f;

    eta
}