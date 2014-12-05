package cz.muni.fi.PV254;

import com.googlecode.jcsv.CSVStrategy;
import com.googlecode.jcsv.reader.CSVReader;
import com.googlecode.jcsv.reader.internal.CSVReaderBuilder;
import com.googlecode.jcsv.reader.internal.DefaultCSVEntryParser;

import java.io.File;
import java.io.FileReader;
import java.io.PrintStream;
import java.util.List;

/**
 * User: VJ
 * Date: 23. 11. 2014
 * Time: 18:01
 */
public class CsvConvert {

    public static void main(String... args) throws Exception {
        convertCSV(new File("blog-post-likes.csv"), new File("blog-post-likes-formatted.csv"));
    }

    public static void convertCSV(File fIn, File fOut) throws Exception {
        PrintStream out = new PrintStream(fOut);
        CSVReader<String[]> csvParser = new CSVReaderBuilder<String[]>(new FileReader(fIn)).strategy(CSVStrategy.UK_DEFAULT).entryParser(new DefaultCSVEntryParser()).build();
        List<String[]> data = csvParser.readAll();

        for (String[] row : data) {
            out.println(String.format("%s,%s", row[1], row[0]));
        }
    }
}
