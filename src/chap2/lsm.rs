use image::Rgb;
use imageproc::drawing::{Canvas};

mod libs;
use crate::libs::lib3d::{get_f0, im_to_log, plot_feature_point, PointLogical};
use libs::lib3d::find_features;

fn main() {
    let input_image_path = "data/chap2/mami2.png";
    let input_ori_image_path = "data/chap2/mami2_ori.png";
    let output_image_path = "result/chap2/mami2.png";

    let img = image::open(input_image_path).unwrap();
    println!("dimensions {:?}", img.dimensions());

    let feature_points = find_features(&img);
    println!("points = {:?}", feature_points.len());

    let f0 = get_f0(&img);
    let fp:Vec<PointLogical> = feature_points.iter().map(|x| im_to_log(x, &f0)).collect();
    println!("points = {:?}", fp.len());

    let mut img_work = image::open(input_ori_image_path).unwrap().to_rgb8();
    plot_feature_point(&mut img_work, feature_points,Rgb([255, 0, 0]), output_image_path);



}
