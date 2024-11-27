char *get_id( IHEAD *head);
void set_id( IHEAD *i, char *path);
char *get_created( IHEAD *head);
void set_created( IHEAD *head);
int get_width( IHEAD *head);
int set_width( IHEAD *head, int width);
int get_height( IHEAD *head);
int set_height( IHEAD *head, int height);
int get_depth( IHEAD *head);
int set_depth( IHEAD *head, int depth);
int get_density( IHEAD *head);
int set_density( IHEAD *head, int density);
int get_compression( IHEAD *head);
int set_compression( IHEAD *head, int compression_code);
int get_complen( IHEAD *head);
int set_complen( IHEAD *head, int complen);
int get_align( IHEAD *head);
int set_align( IHEAD *head, int align);
int get_unitsize( IHEAD *head);
int set_unitsize( IHEAD *head, int unitsize);
int get_sigbit( IHEAD *head);
int set_sigbit( IHEAD *head, int sigbit);
int get_byte_order( IHEAD *head);
int set_byte_order( IHEAD *head, int byte_order);
int get_pix_offset( IHEAD *head);
int set_pix_offset( IHEAD *head, int pix_offset);
int get_whitepix( IHEAD *head);
int set_whitepix( IHEAD *head, int whitepix);
int get_issigned( IHEAD *head);
int set_issigned( IHEAD *head, int issigned);
int get_rm_cm( IHEAD *head);
int set_rm_cm( IHEAD *head, int rm_cm);
int get_tb_bt( IHEAD *head);
int set_tb_bt( IHEAD *head, int tb_bt);
int get_lr_rl( IHEAD *head);
int set_lr_rl( IHEAD *head, int lr_rl);
char *get_parent( IHEAD *head);
void set_parent( IHEAD *i, char *path);
int get_par_x( IHEAD *head);
int set_par_x( IHEAD *head, int par_x);
int get_par_y( IHEAD *head);
int set_par_y( IHEAD *head, int par_y);
