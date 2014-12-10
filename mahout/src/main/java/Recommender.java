import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericBooleanPrefUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

import java.io.File;
import java.util.List;

/**
 * User: PC
 * Date: 28. 11. 2014
 * Time: 20:08
 */
public class Recommender  {

    private UserBasedRecommender recommender;

    public Recommender() {

    }


    private void init() {
        try {

            File jar = new File(Recommender.class.getProtectionDomain().getCodeSource().getLocation().getPath());
            File file = new File(jar.getParent(),"blog-post-likes-formatted.csv");

            DataModel model = new FileDataModel(file);
            UserSimilarity similarity = new LogLikelihoodSimilarity(model);
            UserNeighborhood neighborhood = new NearestNUserNeighborhood(25, similarity, model);
            recommender = new GenericBooleanPrefUserBasedRecommender(model, neighborhood, similarity);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public List<RecommendedItem> recommend(int userId, int numItems) {
        try {
            if(recommender == null){
                init();
            }
            return recommender.recommend(userId, numItems);
        } catch (TasteException e) {
            return null;
        }
    }

    public static void main(String... args) throws Exception {
        Recommender recommender = new Recommender();
        recommender.init();
        List<RecommendedItem> recommendations = recommender.recommend(Integer.parseInt(args[0]), Integer.parseInt(args[1]));
        for(RecommendedItem recommendedItem  : recommendations){
            System.out.println(recommendedItem.getItemID());
        }
    }

}
