import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStream;

import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
//import Package.Extractor;


public class Extractor {
	// TODO Auto-generated method stub
	//String sentence="Newton was born in 1643 in Lincolnshire.";

		public void Extract() throws Exception {
	String sentence1 = "Newton was an English physicist and mathematician. Newton was born in 1643 in Lincolnshire. His father was a prosperous farmer. Newton went to University of Cambridge in 1661. He was interested in mathematics, optics, physics and astronomy. Newton published The Optics in 1704. Newton was elected as member of the parliament in 1689 for University of Cambridge. He was elected president of the Royal Society in 1703. He was a difficult man and prone to depression. He died in 1727 in Westminster Abbey.";
	InputStream inputStream = new FileInputStream("F:\\MindMap_Opennlp_Python\\opennlp\\en-sent.bin"); //byte by byte
	  SentenceModel sentmodel = new SentenceModel(inputStream);    
	  //Instantiating the SentenceDetectorME class 
	  SentenceDetectorME detector = new SentenceDetectorME(sentmodel); //using maximum entropy method to detect sentences and object instantiation
	  String sentences[] = detector.sentDetect(sentence1); 

	for(String sentence : sentences)
	{	
			FileInputStream tokenModelIn = new FileInputStream("F:\\MindMap_Opennlp_Python\\opennlp\\en-token.bin");
	        TokenizerModel tokenModel = new TokenizerModel(tokenModelIn);
	        Tokenizer tokenizer = new TokenizerME(tokenModel);
	        String tokens[] = tokenizer.tokenize(sentence);
	       
	        InputStream posModelIn = new FileInputStream("F:\\MindMap_Opennlp_Python\\opennlp\\en-pos-maxent.bin");
	        POSModel posModel = new POSModel(posModelIn);
	        POSTaggerME posTagger = new POSTaggerME(posModel);
	        String tags[] = posTagger.tag(tokens);

	        InputStream ins = new FileInputStream("F:\\MindMap_Opennlp_Python\\opennlp\\en-chunker.bin");
	        ChunkerModel chunkerModel = new ChunkerModel(ins);
	        ChunkerME chunker = new ChunkerME(chunkerModel);
	        String[] chunks = chunker.chunk(tokens,tags);
	        
	        BufferedWriter writer = new BufferedWriter(new FileWriter("F:\\MindMap_Opennlp_Python\\Mind Map Programs\\outA.txt", true));
	        
	        for(int i=0;i< chunks.length;i++){
	            System.out.println(tokens[i]+" | "+tags[i]+" | "+chunks[i]);
	        }
	        
	        boolean flag=false;
	       
	        for(int i=0;i<chunks.length;i++){
	        	 while(tags[i].contains("NN") && chunks[i].contains("NP"))
	             {
	        		writer.append(tokens[i]);
	        		writer.append(' ');
	             	System.out.print(tokens[i]+" ");
	             	i++;
	                
	             }
	        	 
	        	 writer.newLine();
	        	 writer.append("\t");
	        	 System.out.println("\t");
	        	 
	        	while(chunks[i].contains("VP"))
	        	{
	        		writer.append(tokens[i]);
	        		writer.append(' ');
	        		System.out.println(tokens[i]);
	        		i++;
	        	}
	        	 writer.newLine();
	        	 writer.append("\t\t");
	        	 System.out.println("\t\t");
	        }
			
			writer.close();
			
			

		}
		}



	public static void main(String[] args) throws Exception {
		Extractor extractor = new Extractor();
		extractor.Extract();
		
	}
}
