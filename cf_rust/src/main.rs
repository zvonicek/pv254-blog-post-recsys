extern crate csv;
use std::collections::HashMap;
use std::collections::TreeMap;
use std::collections::HashSet;
use std::collections::hash_map::Occupied;
use std::collections::hash_map::Vacant;


fn main() {
    println!(">> RECSYS welcome!");

    let current_user_id = 20930;

    let fp = &Path::new("./../data/blog-post-likes.csv");
    let mut rdr = csv::Reader::from_file(fp);
    let mut data: HashMap<uint, HashSet<uint>> = HashMap::new();
    let mut need_ratings: HashSet<uint> = HashSet::new();
    let mut predictions: TreeMap<uint, uint> = TreeMap::new();

    let mut i = 0i;
    for record in rdr.decode() {
        let (post_id, user_id): (uint, uint) = record.unwrap();

        match data.entry(post_id) {
            Vacant(entry) => entry.set(HashSet::new()),
            Occupied(entry) => entry.into_mut(),
        }.insert(user_id);
        
        if user_id != current_user_id {
            need_ratings.insert(post_id);
        }

        i += 1;
        if i > 10000 {
            break;
        }
    }


    for i in need_ratings.iter() {
        let mut prediction = 0f32;

        for j in data.keys() {
            let set_a = data.get(i).unwrap();
            let set_b = data.get(j).unwrap();

            let f_a = set_a.len() as f32;
            let f_b = set_b.len() as f32;
            let f_both = set_a.intersection(set_b).count() as f32;

            let s = f_both / (f_a * f_b);

            prediction += s;
        }
        
        predictions.insert((prediction * 1000.0).round() as uint, *i);
    }


    let mut i = 0i;
    println!("prediction, rating");
    for (prediction, post_id) in predictions.rev_iter() {
        println!("{}: {}", prediction, post_id);
        i += 1;
        if i > 10 {
            break;
        }
    }


    println!(">> DONE! Bey");
}
