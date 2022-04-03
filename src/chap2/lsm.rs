use image::Rgb;
use imageproc::drawing::{Canvas, draw_filled_circle_mut};

mod libs;
use crate::libs::lib3d::{plot_feature_point, PointImage};
use libs::lib3d::find_features;

fn main() {
    let input_image_path = "data/chap2/mami1.png";
    let input_ori_image_path = "data/chap2/mami1_ori.png";
    let output_image_path = "result/chap2/mami1.png";

    let img = image::open(input_image_path).unwrap();
    println!("dimensions {:?}", img.dimensions());

    let feature_points = find_features(&img);
    println!("points = {:?}", feature_points.len());

    let mut img_work = image::open(input_ori_image_path).unwrap().to_rgb8();
    plot_feature_point(&mut img_work, feature_points,Rgb([255, 0, 0]), output_image_path);



}
