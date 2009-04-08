#include "Image.h"
#include "xtprobeImageFile.h"
#include "TensorFile.h"
#include "ipBlock.h"
#include "CmdLine.h"

using namespace Torch;


int main(int argc, char* argv[])
{
        ///////////////////////////////////////////////////////////////////
        // Parse the command line
        ///////////////////////////////////////////////////////////////////

	// Set options
        char* tensor_filename;
        char* output_basename;
	bool verbose;
	int block_size_h;
	int block_size_w;
	int block_overlap_h;
	int block_overlap_w;

	// Build the command line object
	CmdLine cmd;
	cmd.setBOption("write log", false);

	cmd.info("Tensor read program");

	cmd.addText("\nArguments:");
	cmd.addSCmdArg("tensor file to test", &tensor_filename, "tensor file to read");

	cmd.addText("\nBlock decomposition:");
	cmd.addICmdOption("-sizeH", &block_size_h, 8, "block size H");
	cmd.addICmdOption("-sizeW", &block_size_w, 8, "block size W");
	cmd.addICmdOption("-overlapH", &block_overlap_h, 4, "overlap H between blocks");
	cmd.addICmdOption("-overlapW", &block_overlap_w, 4, "overlap W between blocks");

	cmd.addText("\nOptions:");
	cmd.addBCmdOption("-verbose", &verbose, false, "print Tensor values");
	cmd.addSCmdOption("-o", &output_basename, "block", "basename");

	// Parse the command line
	if (cmd.read(argc, argv) < 0)
	{
		return 0;
	}

	TensorFile tf;

	CHECK_FATAL(tf.openRead(tensor_filename));

	print("Reading tensor header file ...\n");
	const TensorFile::Header& header = tf.getHeader();

	print("Tensor file:\n");
	print(" type:         [%s]\n", str_TensorTypeName[header.m_type]);
	print(" n_tensors:    [%d]\n", header.m_n_samples);
	print(" n_dimensions: [%d]\n", header.m_n_dimensions);
	print(" size[0]:      [%d]\n", header.m_size[0]);
	print(" size[1]:      [%d]\n", header.m_size[1]);
	print(" size[2]:      [%d]\n", header.m_size[2]);
	print(" size[3]:      [%d]\n", header.m_size[3]);

	if(header.m_type != Tensor::Short)
	{
		warning("Unsupported tensor type (Short only).");

		return 1;
	}

	if(header.m_n_dimensions != 2)
	{
		warning("Unsupported dimensions (2 only).");

		return 1;
	}

	//
	ipBlock ipblock;

	ipblock.setBOption("rcoutput", true);
	ipblock.setIOption("ox", block_overlap_w);
	ipblock.setIOption("oy", block_overlap_h);
	ipblock.setIOption("w", block_size_w);
	ipblock.setIOption("h", block_size_h);
		
	//
	Tensor *tensor = NULL;
	char ofilename[250];

	TensorFile *ofile = new TensorFile;
	sprintf(ofilename, "%s.tensor", output_basename);
	ofile->openWrite(ofilename, Tensor::Short, 2, block_size_h, block_size_w, 0, 0);

	for(int t = 0 ; t < header.m_n_samples ; t++)
	{
		tensor = tf.load();

		Image imagegray(tensor->size(1), tensor->size(0), 1);
		ShortTensor *t_ = new ShortTensor();
		t_->select(&imagegray, 2, 0);
		t_->copy(tensor);

		ipblock.process(imagegray);

		print("Number of output blocks: %d\n", ipblock.getNOutputs());

		ShortTensor &t_rcoutput = (ShortTensor &) ipblock.getOutput(0);
		int n_rows = t_rcoutput.size(0);
		int n_cols = t_rcoutput.size(1);

		ShortTensor *t_rcoutput_narrow_rows = new ShortTensor();
		ShortTensor *t_rcoutput_narrow_cols = new ShortTensor();
		ShortTensor *t_block = new ShortTensor(block_size_h, block_size_w);

		for(int r = 0; r < n_rows; r++)
		{
			t_rcoutput_narrow_rows->narrow(&t_rcoutput, 0, r, 1);

		   	for(int c = 0; c < n_cols; c++) 
			{
				t_rcoutput_narrow_cols->narrow(t_rcoutput_narrow_rows, 1, c, 1);
		
				/* normally here we should not be able to this as
					t_rcoutput_narrow_cols is a 4D tensor and t_block is a 2D tensor

				   however, as t_rcoutput_narrow_cols is narrowed along row and col to a lenght of 1
				   it is possible.

				   For more details, look at src/ip/ipBlock.cc
				*/
				t_block->copy(t_rcoutput_narrow_cols);

				ofile->save(*t_block);
			}
		}
	
		delete t_block;
		delete t_rcoutput_narrow_cols;
		delete t_rcoutput_narrow_rows;

		delete t_;
		delete tensor;
	}

	tf.close();

	delete ofile;

        // OK
	return 0;
}

