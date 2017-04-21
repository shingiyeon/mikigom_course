class AppleBox{
	private:
		int num_apple;
		int size_of_box;
	public:
		AppleBox();
		void set_box_size(int size);
		void set_num_apple(int n);
		void add_one_apple(void);
		void remove_one_apple(void);
		int get_num_apple(void);
		int get_box_size(void);
		bool is_empty(void);
		bool is_full(void);
};
