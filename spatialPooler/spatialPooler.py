 i m p o r t   H T M S e t t i n g s  
 i m p o r t   u t i l s  
  
 _ _ a u t h o r _ _   =   ' A V P e t r o v '  
 i m p o r t   r a n d o m  
 f r o m   r e g i o n   i m p o r t   R e g i o n  
  
 c l a s s   S p a t i a l P o o l e r :  
         d e f   _ _ i n i t _ _ ( s e l f ,   s e t t i n g s ) :  
                 s e l f . s e t t i n g s   =   s e t t i n g s  
                 s e l f . r   =   r a n d o m . R a n d o m ( )  
                 s e l f . r . s e e d   =   1 0  
                 s e l f . a c t i v e D u t y C y c l e s   =   [ ]  
                 s e l f . o v e r l a p D u t y C y c l e s   =   [ ]  
                 #   t h i s . s e t t i n g s = s e t t i n g s ;  
                 #   a c t i v e D u t y C y c l e s = n e w   i n t [ s e t t i n g s . x D i m e n s i o n * s e t t i n g s . y D i m e n s i o n ] ;  
                 #   o v e r l a p D u t y C y c l e s = n e w   i n t [ s e t t i n g s . x D i m e n s i o n * s e t t i n g s . y D i m e n s i o n ] ;  
  
         d e f   g e t A c t i v e D u t y C y c l e s ( s e l f ) :  
                 r e t u r n   s e l f . a c t i v e D u t y C y c l e s  
  
  
         d e f   f i n d B y C o l I n d e x ( s e l f ,   c o l s ,   i n d e x ) :  
                 f o r   c   i n   c o l s :  
                         i f ( c . g e t I n d e x ( ) = = i n d e x ) :   r e t u r n   c  
                 r e t u r n   N o n e  
  
  
         d e f   u p d a t e O v e r l a p s ( c o l s ,   i n p u t ) :  
                 o v e r l a p s = [ 0   f o r   i   i n   r a n g e ( l e n ( c o l s ) ) ]  
                 i = 0  
                 f o r   c   i n   c o l s :  
                         f o r   s   i n   c . g e t C o n n e c t e d S y n a p s e s ( ) :  
                                 o v e r l a p s [ i ] = o v e r l a p s [ i ]   +   ( i n p u t . g e t ( s . g e t I n d e x C o n n e c t T o ( ) )   i f   1   e l s e   0 )  
                         i = i + 1  
                 r e t u r n   o v e r l a p s  
  
  
         d e f   i n h i b i t i o n P h a s e ( s e l f ,   c o l s ,   o v e r l a p s ) :  
                 a c t i v e C o l u m n s = [ ]  
  
                 i n d e x i e s   =   [ i   f o r   i   i n   r a n g e ( l e n ( c o l s ) ) ]  
                 s e l f . r . s h u f f l e ( i n d e x i e s )  
                 f o r   i n d x   i n   i n d e x i e s :  
                         c o l u m n = c o l s . g e t ( i n d x )  
                         i f   c o l u m n . g e t N e i g h b o r s ( ) . s i z e ( )   >   0 :  
  
                                 n e i g h b o r O v e r l a p s   =   [ o v e r l a p s [ i ]   f o r   i   i n   c o l u m n . g e t N e i g h b o r s ( ) ]  
  
                                 m i n L o c a l O v e r l a p   =   u t i l s . k t h S c o r e ( n e i g h b o r O v e r l a p s ,   s e l f . s e t t i n g s . d e s i r e d L o c a l A c t i v i t y )  
  
  
                                 i f   o v e r l a p s [ c o l u m n . g e t I n d e x ( ) ]   >   0   a n d   o v e r l a p s [ c o l u m n . g e t I n d e x ( ) ]   > =   m i n L o c a l O v e r l a p :  
  
                                         n = 0  
                                         f o r   i   i n   c o l u m n . g e t N e i g h b o r s ( ) :  
                                                 n = n + ( s e l f . f i n d B y C o l I n d e x ( c o l s , i ) . i s A c t i v e ( )   i f     1   e l s e   0 )  
                                         i f   n < = ( s e l f . s e t t i n g s . d e s i r e d L o c a l A c t i v i t y - 1 ) :  
                                                 c o l u m n . s e t I s A c t i v e ( T r u e )  
                                                 a c t i v e C o l u m n s . a d d ( c o l u m n )  
                                 e l s e :  
                                         c o l u m n . s e t I s A c t i v e ( F a l s e )  
  
                 r e t u r n   a c t i v e C o l u m n s  
  
  
  
  
  
         d e f   u p d a t e S y n a p s e s ( c o l s , i n p u t ) :  
                 f o r   c o l   i n   c o l s :  
                         f o r   s y n a p s e   i n   c o l . g e t P o t e n t i a l S y n a p s e s ( ) . v a l u e s ( ) :  
                                 i f   i n p u t . g e t ( s y n a p s e . g e t I n d e x C o n n e c t T o ( ) ) :  
                                         s y n a p s e . i n c r e a s e P e r m a n e n c e ( )  
                                 e l s e :  
                                         s y n a p s e . d e c r e a s e P e r m a n e n c e ( )  
  
         d e f   u p d a t e A c t i v e D u t y C y c l e ( s e l f , c o l s ) :  
                 f o r   i   i n   r a n g e ( l e n ( c o l s ) ) :  
                         s e l f . a c t i v e D u t y C y c l e s [ i ]   =   s e l f . a c t i v e D u t y C y c l e s [ i ]   +   ( c o l s . g e t ( i ) . i s A c t i v e ( )   i f   1   e l s e   0 )  
  
  
         d e f   u p d a t e O v e r l a p D u t y C y c l e ( s e l f , c o l , o v e r l a p s ) :  
                 s e l f . o v e r l a p D u t y C y c l e s [ c o l . g e t I n d e x ( ) ]   =   s e l f . o v e r l a p D u t y C y c l e s [ c o l . g e t I n d e x ( ) ]   +   ( o v e r l a p s [ c o l . g e t I n d e x ( ) ]   >   s e l f . s e t t i n g s . m i n O v e r l a p   i f   1   e l s e   0 )  
  
  
  
         d e f   u p d a t e B o o s t F a c t o r ( s e l f , c o l ,   m i n V a l u e ) :  
                 v a l u e   =   1  
  
                 i f   ( s e l f . a c t i v e D u t y C y c l e s [ c o l . g e t I n d e x ( ) ]   <   m i n V a l u e ) :  
                                 v a l u e   =   1   +   ( m i n V a l u e   -   s e l f . a c t i v e D u t y C y c l e s [ c o l . g e t I n d e x ( ) ] )   *   ( s e l f . s e t t i n g s . m a x B o o s t   -   1 )  
                 c o l . s e t B o o s t F a c t o r ( v a l u e )  
  
  
         d e f   l e a r n i n g P h a s e ( s e l f , c o l s ,   i n p u t , o v e r l a p s ) :  
  
                 s e l f . u p d a t e S y n a p s e s ( c o l s , i n p u t )  
  
                 f o r   c o l u m n   i n   c o l s :  
                         m a x A c t i v e D u t y   =   0  
                         f o r   i n d e x   i n   c o l u m n . g e t N e i g h b o r s ( ) :  
                                 m a x A c t i v e D u t y   =   m a x A c t i v e D u t y   >   s e l f . a c t i v e D u t y C y c l e s [ i n d e x ]   i f   m a x A c t i v e D u t y   e l s e   s e l f . a c t i v e D u t y C y c l e s [ i n d e x ]  
  
                         m i n D u t y C y c l e   =   s e l f . s e t t i n g s . m i n D u t y C y c l e F r a c t i o n   *   m a x A c t i v e D u t y  
  
                         s e l f . u p d a t e B o o s t F a c t o r ( c o l u m n , m i n D u t y C y c l e )  
  
                         s e l f . u p d a t e O v e r l a p D u t y C y c l e ( c o l u m n , o v e r l a p s )  
                         i f   s e l f . o v e r l a p D u t y C y c l e s [ c o l u m n . g e t I n d e x ( ) ]   <   m i n D u t y C y c l e :  
                                 c o l u m n . s t i m u l a t e ( )  
  
                 s e l f . u p d a t e A c t i v e D u t y C y c l e ( c o l s )  
  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
 f r o m   m a p p e r s . V e r y S i m p l e M a p p e r   i m p o r t   v e r y S i m p l e M a p p e r  
 f r o m   m a p p e r s . S i m p l e M a p p e r   i m p o r t   s i m p l e M a p p e r  
  
  
  
  
  
         #   p u b l i c   v o i d   t e s t D i f f ( )   t h r o w s   I O E x c e p t i o n  
         #   {  
         #           F i l e I n p u t S t r e a m   f i s _ t r u t h = n e w   F i l e I n p u t S t r e a m ( " i n . t x t " ) ;  
         #           S c a n n e r   s c _ t r u t h = n e w   S c a n n e r ( f i s _ t r u t h ) ;  
         #           F i l e I n p u t S t r e a m   f i s _ p r e d i c t = n e w   F i l e I n p u t S t r e a m ( " o u t _ p r e d i c t . t x t " ) ;  
         #           S c a n n e r   s c _ p = n e w   S c a n n e r ( f i s _ p r e d i c t ) ;  
         #           F i l e O u t p u t S t r e a m   f o s _ e r r = n e w   F i l e O u t p u t S t r e a m ( " e r r s . t x t " ) ;  
         #           P r i n t W r i t e r   p w _ e r r = n e w   P r i n t W r i t e r ( f o s _ e r r ) ;  
         #  
         #  
         #  
         #           i n t   w = s c _ t r u t h . n e x t I n t ( ) ;  
         #           i n t   h = s c _ t r u t h . n e x t I n t ( ) ;  
         #           i n t   s t e p = s c _ t r u t h . n e x t I n t ( ) ;  
         #  
         #           s c _ t r u t h . n e x t L i n e ( ) ;  
         #           s c _ p . n e x t L i n e ( ) ;  
         #  
         #           f o r ( i n t   s = 0 ; s < s t e p ; s + + )   {  
         #                   i n t [ ]   e r r s = n e w   i n t [ h ] ;  
         #                   f o r   ( i n t   i   =   0 ;   i   <   h ;   i + + )   {  
         #                           B i t V e c t o r   t r u e _ b v = M a t h U t i l s . b i t v e c t o r F r o m S t r i n g ( s c _ t r u t h . n e x t L i n e ( ) ) ;  
         #                           / / S y s t e m . o u t . p r i n t l n ( s c _ t r u t h . n e x t L i n e ( ) ) ;  
         #                           B i t V e c t o r   p r e d i c t _ b v = M a t h U t i l s . b i t v e c t o r F r o m S t r i n g ( s c _ p . n e x t L i n e ( ) ) ;  
         #                           / / S y s t e m . o u t . p r i n t l n ( s c _ p . n e x t L i n e ( ) ) ;  
         #  
         #                           p r e d i c t _ b v . x o r ( t r u e _ b v ) ;  
         #                           e r r s [ i ] = ( i n t ) M a t h U t i l s . s u m O f L o n g s ( p r e d i c t _ b v . e l e m e n t s ( ) ) ;  
         #                   }  
         #                   p w _ e r r . p r i n t l n ( M a t h U t i l s . s u m O f I n t s ( e r r s ) ) ;  
         #           }  
         #           p w _ e r r . c l o s e ( ) ;  
         #   }  
  
  
 d e f   f i n d B y C o l X Y ( c o l s ,   x ,   y ) :  
         f o r   c   i n   c o l s :  
                 v = c . g e t C o o r d ( ) ;  
                 i f ( v . g e t X ( ) = = x   a n d   v . g e t Y ( ) = = y ) :   r e t u r n   c ;  
  
         r e t u r n   N o n e ;  
  
 f r o m   e n u m   i m p o r t   E n u m  
 c l a s s   D i r ( E n u m ) :  
         U P = 1  
         D O W N = 2  
  
 d e f   t e s t L a d d e r ( ) :  
  
                 #   F i l e O u t p u t S t r e a m   f o s = n e w   F i l e O u t p u t S t r e a m ( " o u t . t x t " ) ;  
                 #   P r i n t W r i t e r   p w = n e w   P r i n t W r i t e r ( f o s ) ;  
  
                 #   F i l e O u t p u t S t r e a m   f o s _ i n = n e w   F i l e O u t p u t S t r e a m ( " i n . t x t " ) ;  
                 #   P r i n t W r i t e r   p w _ i n = n e w   P r i n t W r i t e r ( f o s _ i n ) ;  
  
                 W = 9 5  
                 H = 9 5  
                 b e g X = 0  
                 b e g Y = 0  
                 s t e p S i z e = 2 0  
  
                 m a p   =   [ [ ] ]  
                 m y A r r a y = [ [ 0   f o r   j   i n   H ]   f o r   i   i n   W ]  
                 i n p = [ ]  
                 i n p = [ 0   f o r   i   i n   H * W ]  
                 S T E P S = 2 5 ;  
                 T O T A L _ S T E P S = 1 0 0 0 ;  
                 S T E P _ S I Z E = S T E P S ;  
  
                 s e t t i n g = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
                 s e t t i n g . d e b u g = T r u e ;  
  
                 s e t t i n g . a c t i v a t i o n T h r e s h o l d   =   1 ;  
                 s e t t i n g . m i n O v e r l a p   =   1 ;  
                 s e t t i n g . d e s i r e d L o c a l A c t i v i t y   =   3 ;  
                 s e t t i n g . c o n n e c t e d P c t = 1 ;  
                 s e t t i n g . c o n n e c t e d P e r m = 0 . 0 1 ;  
                 s e t t i n g . x I n p u t = W ;  
                 s e t t i n g . y I n p u t = H ;  
                 s e t t i n g . p o t e n t i a l R a d i u s = 4 ;  
                 s e t t i n g . x D i m e n s i o n = 1 0 ;  
                 s e t t i n g . y D i m e n s i o n = 1 0 ;  
                 s e t t i n g . i n i t i a l I n h i b i t i o n R a d i u s = 1 ;  
  
                 #   p w . p r i n t ( s e t t i n g . x D i m e n s i o n   +   "   " ) ;  
                 #   p w . p r i n t ( s e t t i n g . y D i m e n s i o n   +   "   " ) ;  
                 #   p w . p r i n t ( T O T A L _ S T E P S ) ;  
                 #   p w . p r i n t l n ( ) ;  
                 #  
                 #   p w _ i n . p r i n t ( s e t t i n g . x D i m e n s i o n   +   "   " ) ;  
                 #   p w _ i n . p r i n t ( s e t t i n g . y D i m e n s i o n   +   "   " ) ;  
                 #   p w _ i n . p r i n t ( T O T A L _ S T E P S ) ;  
                 #   p w _ i n . p r i n t l n ( ) ;  
  
                 r = R e g i o n ( s e t t i n g , v e r y S i m p l e M a p p e r ( ) ) ;  
  
                 s p = S p a t i a l P o o l e r ( s e t t i n g ) ;  
  
  
                 x = b e g X , y = b e g Y  
                 f o r     i   i n   r a n g e ( x , x + s t e p S i z e ) :  
                         f o r     j   i n   r a n g e ( y , y + s t e p S i z e ) :  
                                 m a p [ i ] [ j ]   =   1 ;  
  
                 f o r   s t e p   i n   r a n g e ( T O T A L _ S T E P S ) :  
                         p r i n t ( " D A T A : \ n " ) ;  
                         i n d e x   =   0 ;  
                         f o r   k   i n   r a n g e ( W ) :  
                                 f o r   m   i n   r a n g e ( H ) :  
                                         i n p [ i n d e x ]   =   m a p [ k ] [ m ] ;  
                                         #   p w _ i n . p r i n t ( i n [ i n d e x ] ) ;  
                                         i n d e x = i n d e x + 1 ;  
                                 #   p w _ i n . p r i n t l n ( )  
                         #   p w _ i n . p r i n t l n ( ) ;  
  
                         f o r     i   i n   r a n g e ( x , x + s t e p S i z e ) :  
                                 f o r     j   i n   r a n g e ( y , y + s t e p S i z e ) :  
                                         i f   i < l e n ( m a p )   a n d   j < l e n ( m a p [ 0 ] ) :  
                                                 m a p [ i ] [ j ]   =   0  
  
                         x = x + S T E P _ S I Z E ;  
                         y = y + S T E P _ S I Z E ;  
                         i f ( x > W ) :  
                                 x = 0 ;  
                                 y = 0 ;  
  
                         f o r     i   i n   r a n g e ( x , x + s t e p S i z e ) :  
                                 f o r     j   i n   r a n g e ( y , y + s t e p S i z e ) :  
                                         i f   i < l e n ( m a p )   a n d   j < l e n ( m a p [ 0 ] ) :  
                                                 m a p [ i ] [ j ]   =   1  
  
                         f o r   c   i n   r . g e t C o l u m n s ( ) :  
                                 c . s e t I s A c t i v e ( F a l s e ) ;  
                         o v = s p . u p d a t e O v e r l a p s ( r . g e t C o l u m n s ( ) ,   i n p u t ) ;  
                         s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v ) ;  
                         s p . l e a r n i n g P h a s e ( r . g e t C o l u m n s ( ) ,   i n p u t ,   o v ) ;  
  
  
                         c o l s = r . g e t C o l u m n s ( ) ;  
                         f o r   i   i n   r a n g e ( s e t t i n g . x D i m e n s i o n ) :  
                                 f o r   j   i n   r a n g e ( s e t t i n g . y D i m e n s i o n ) :  
                                         s t a t e = f i n d B y C o l X Y ( c o l s , i , j ) . i s A c t i v e ( )   i f   1   e l s e   0 ;  
                                         #   p w . p r i n t ( s t a t e ) ;  
                                         #   p w . p r i n t ( "   " ) ;  
                                 #   p w . p r i n t l n ( ) ;  
                         #   p w . p r i n t l n ( ) ;  
  
                         #   / * S y s t e m . o u t . p r i n t l n ( " B O O S T : " ) ;  
                         #   c o l s = r . g e t C o l u m n s ( ) ;  
                         #   f o r ( i n t   i = 0 ; i < s e t t i n g s . x D i m e n s i o n ; i + + )  
                         #   {  
                         #           f o r ( i n t   j = 0 ; j < s e t t i n g s . y D i m e n s i o n ; j + + )   {  
                         #                   S y s t e m . o u t . p r i n t ( c o l s . g e t ( i * s e t t i n g s . y D i m e n s i o n + j ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t B o o s t F a c t o r ( ) + "   " ) ;  
                         #           }  
                         #           S y s t e m . o u t . p r i n t l n ( ) ;  
                         #   } * /  
                 #   p w . c l o s e ( ) ;  
  
 #           d e f   t e s t L e a r n i n g ( )  
 #           {  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 1 , 1 , 1 , 1 , 0 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #                   s e t t i n g s . i n i t i a l I n h i b i t i o n R a d i u s = 1 ;  
 #                   s e t t i n g s . p e r m a n e n c e I n c = 0 . 2 ;  
 #                   s e t t i n g s . p e r m a n e n c e D e c = 0 . 2 ;  
 #  
 #                   R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #                   S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 4 ) . s e t P e r m a n e n c e ( 0 . 5 ) ;  
 #                   r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 5 ) . s e t P e r m a n e n c e ( 0 . 5 ) ;  
 #                   i n t [ ]   o v = s p . u p d a t e O v e r l a p s ( r . g e t C o l u m n s ( ) ,   i n p u t ) ;  
 #                   s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) , o v ) ;  
 #                   s p . l e a r n i n g P h a s e ( r . g e t C o l u m n s ( ) ,   i n p u t ,   o v ) ;  
 #  
 #                   d o u b l e   v = r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 4 ) . g e t P e r m a n e n c e ( ) ;  
 #                   A s s e r t . a s s e r t T r u e ( v   = =   0 . 7 ) ;  
 #                   v = r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 5 ) . g e t P e r m a n e n c e ( ) ;  
 #                   A s s e r t . a s s e r t T r u e ( v   = =   0 . 3 ) ;  
 #  
 #           }  
 #  
 #           p u b l i c   v o i d   t e s t U p d a t e A c t i v e D u t y C y c l e ( )   {  
 #                   M e t h o d   m e t h o d   =   n u l l ;  
 #                   t r y   {  
 #                           M e t h o d [ ]   m   =   S p a t i a l P o o l e r . c l a s s . g e t M e t h o d s ( ) ;  
 #                           m e t h o d   =   S p a t i a l P o o l e r . c l a s s . g e t D e c l a r e d M e t h o d ( " u p d a t e A c t i v e D u t y C y c l e " ,   A r r a y L i s t . c l a s s ) ;  
 #                   }   c a t c h   ( N o S u c h M e t h o d E x c e p t i o n   e )   {  
 #                           e . p r i n t S t a c k T r a c e ( ) ;  
 #                   }  
 #                   m e t h o d . s e t A c c e s s i b l e ( t r u e ) ;  
 #  
 #  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #                   s e t t i n g s . i n i t i a l I n h i b i t i o n R a d i u s = 1 ;  
 #                   t r y   {  
 #                           R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #  
 #                           S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                           i n t [ ]   o v e r l a p s = s p . u p d a t e O v e r l a p s ( r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) . l e n g t h   = =   r . g e t C o l u m n s ( ) . s i z e ( ) ) ;  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) [ 0 ]   = =   4 ) ;  
 #  
 #  
 #                           i n = n e w   i n t [ ] { 1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 } ;  
 #                           i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                           M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                           r = n e w   R e g i o n ( s e t t i n g s ,   n e w   S i m p l e M a p p e r ( ) ) ;  
 #                           s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                           o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #                           s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                           m e t h o d . i n v o k e ( s p ,   r . g e t C o l u m n s ( ) ) ;  
 #  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) . l e n g t h   = =   r . g e t C o l u m n s ( ) . s i z e ( ) ) ;  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) [ 0 ] = = 0 ) ;  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) [ 1 ] = = 3 ) ;  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) [ 2 ] = = 3 ) ;  
 #                           A s s e r t . a s s e r t T r u e ( s p . g e t A c t i v e D u t y C y c l e s ( ) [ 3 ] = = 2 ) ;  
 #  
 #                   }   c a t c h   ( I l l e g a l A c c e s s E x c e p t i o n   e )   {  
 #                           e . p r i n t S t a c k T r a c e ( ) ;  
 #                   }   c a t c h   ( I n v o c a t i o n T a r g e t E x c e p t i o n   e )   {  
 #                           e . p r i n t S t a c k T r a c e ( ) ;  
 #                   }  
 #           }  
 #  
 #           p u b l i c   v o i d   t e s t U p d a t e S y n a p s e s ( )   {  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 1 , 1 , 1 , 1 , 0 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #                   s e t t i n g s . i n i t i a l I n h i b i t i o n R a d i u s = 1 ;  
 #                   s e t t i n g s . p e r m a n e n c e I n c = 0 . 2 ;  
 #                   s e t t i n g s . p e r m a n e n c e D e c = 0 . 2 ;  
 #                   R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #  
 #                   S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 4 ) . s e t P e r m a n e n c e ( 0 . 5 ) ;  
 #                   s p . u p d a t e S y n a p s e s ( r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                   d o u b l e   v = r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 4 ) . g e t P e r m a n e n c e ( ) ;  
 #                   A s s e r t . a s s e r t T r u e ( v = = 0 . 7 ) ;  
 #  
 #  
 #                   r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 5 ) . s e t P e r m a n e n c e ( 0 . 5 ) ;  
 #                   s p . u p d a t e S y n a p s e s ( r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                   v = r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t P r o x i m a l D e n d r i t e ( ) . g e t P o t e n t i a l S y n a p s e s ( ) . g e t ( 5 ) . g e t P e r m a n e n c e ( ) ;  
 #                   A s s e r t . a s s e r t T r u e ( v = = 0 . 3 ) ;  
 #           }  
 #  
 #           p u b l i c   v o i d   t e s t I n h i b i t i o n P h a s e ( )   {  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #                   s e t t i n g s . i n i t i a l I n h i b i t i o n R a d i u s = 1 ;  
 #  
 #                   R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #  
 #                   S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   s p . s e e d = 1 0 ;  
 #                   i n t [ ]   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                   A r r a y L i s t < C o l u m n >   c o l s = s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #  
 #                   A s s e r t . a s s e r t T r u e ( c o l s . s i z e ( ) = = 2 ) ;  
 #  
 #                   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #                   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #                   c o l s = s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                   A s s e r t . a s s e r t T r u e ( c o l s . s i z e ( ) = = 2 ) ;  
 #                   c o l s = s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                   A s s e r t . a s s e r t T r u e ( c o l s . s i z e ( ) = = 2 ) ;  
 #                   c o l s = s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                   A s s e r t . a s s e r t T r u e ( c o l s . s i z e ( ) = = 2 ) ;  
 #                   c o l s = s p . i n h i b i t i o n P h a s e ( r . g e t C o l u m n s ( ) ,   o v e r l a p s ) ;  
 #                   A s s e r t . a s s e r t T r u e ( c o l s . s i z e ( ) = = 1 ) ;  
 #           }  
 #  
 #           p u b l i c   v o i d   t e s t O v e r l a p O n O n e s ( )   {  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 ,   1 , 1 , 1 , 1 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #  
 #                   R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #  
 #                   S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   i n t [ ]   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #  
 #                   i n t [ ]   g r o u n d t r u t h = n e w   i n t [ ] { 5 , 5 , 5 , 5 } ;  
 #                   f o r   ( i n t   i   =   0 ;   i   <   g r o u n d t r u t h . l e n g t h ;   i + + )  
 #                           a s s e r t T r u e ( o v e r l a p s [ i ] = = g r o u n d t r u t h [ i ] ) ;  
 #  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 1 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #  
 #                   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #                   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #  
 #                   g r o u n d t r u t h = n e w   i n t [ ] { 5 } ;  
 #                   f o r   ( i n t   i   =   0 ;   i   <   g r o u n d t r u t h . l e n g t h ;   i + + )  
 #                           a s s e r t T r u e ( o v e r l a p s [ i ] = = g r o u n d t r u t h [ i ] ) ;  
 #  
 #  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 1 6 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #  
 #                   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #                   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #  
 #                   g r o u n d t r u t h = n e w   i n t [ ] { 3 , 4 , 5 , 5 ,   5 , 5 , 5 , 5 ,   5 , 5 , 5 , 5 ,   5 , 5 , 4 , 3 } ;  
 #                   f o r   ( i n t   i   =   0 ;   i   <   g r o u n d t r u t h . l e n g t h ;   i + + )  
 #                           a s s e r t T r u e ( o v e r l a p s [ i ] = = g r o u n d t r u t h [ i ] ) ;  
 #           }  
 #  
 #           p u b l i c   v o i d   t e s t O v e r l a p O n N o t O n e s ( )   {  
 #                   i n t [ ]   i n = n e w   i n t [ ] { 1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 ,   1 , 0 , 1 , 0 } ;  
 #                   B i t V e c t o r   i n p u t = n e w   B i t V e c t o r ( i n . l e n g t h ) ;  
 #                   M a t h U t i l s . a s s i g n ( i n p u t ,   i n ) ;  
 #  
 #                   H T M S e t t i n g s   s e t t i n g s = H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( ) ;  
 #                   H T M S e t t i n g s . d e b u g = t r u e ;  
 #  
 #                   s e t t i n g s . a c t i v a t i o n T h r e s h o l d   =   1 ;  
 #                   s e t t i n g s . m i n O v e r l a p   =   1 ;  
 #                   s e t t i n g s . d e s i r e d L o c a l A c t i v i t y   =   1 ;  
 #                   s e t t i n g s . c o n n e c t e d P c t = 1 ;  
 #                   s e t t i n g s . x I n p u t = i n p u t . s i z e ( ) ;  
 #                   s e t t i n g s . y I n p u t = 1 ;  
 #                   s e t t i n g s . p o t e n t i a l R a d i u s = 2 ;  
 #                   s e t t i n g s . x D i m e n s i o n = 4 ;  
 #                   s e t t i n g s . y D i m e n s i o n = 1 ;  
 #  
 #                   R e g i o n   r = n e w   R e g i o n ( s e t t i n g s , n e w   S i m p l e M a p p e r ( ) ) ;  
 #  
 #                   S p a t i a l P o o l e r   s p = n e w   S p a t i a l P o o l e r ( s e t t i n g s ) ;  
 #                   i n t [ ]   o v e r l a p s = s p . u p d a t e O v e r l a p s (   r . g e t C o l u m n s ( ) , i n p u t ) ;  
 #  
 #                   i n t [ ]   g r o u n d t r u t h = n e w   i n t [ ] { 3 , 2 ,   3 , 2 } ;  
 #                   f o r   ( i n t   i   =   0 ;   i   <   g r o u n d t r u t h . l e n g t h ;   i + + )  
 #                           a s s e r t T r u e ( o v e r l a p s [ i ] = = g r o u n d t r u t h [ i ] ) ;  
 #           }  
 #  
 d e f   t e s t H T M C o n s t r u c t u i o n ( ) :  
         s e t t i n g   =   H T M S e t t i n g s . H T M S e t t i n g s . g e t D e f a u l t S e t t i n g s ( )  
         s e t t i n g . d e b u g   =   T r u e  
  
         s e t t i n g . a c t i v a t i o n T h r e s h o l d   =   1  
         s e t t i n g . m i n O v e r l a p   =   1  
         s e t t i n g . d e s i r e d L o c a l A c t i v i t y   =   1  
         s e t t i n g . c o n n e c t e d P c t   =   1  
         s e t t i n g . x I n p u t   =   5  
         s e t t i n g . y I n p u t   =   1  
         s e t t i n g . p o t e n t i a l R a d i u s   =   2  
         s e t t i n g . x D i m e n s i o n   =   4  
         s e t t i n g . y D i m e n s i o n   =   1  
         s e t t i n g . i n i t i a l I n h i b i t i o n R a d i u s = 2  
  
  
         r   =   R e g i o n ( s e t t i n g , s i m p l e M a p p e r ( ) )  
  
         a s s e r t   r . g e t C o l u m n s ( ) . s i z e ( )   = =   4  
         a s s e r t   r . g e t I n p u t H ( )   = =   1  
         a s s e r t   r . g e t I n p u t W ( )   = =   5  
         a s s e r t   r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t N e i g h b o r s ( ) . s i z e ( ) = = 2  
         v = r . g e t C o l u m n s ( ) . g e t ( r . g e t C o l u m n s ( ) . g e t ( 0 ) . g e t N e i g h b o r s ( ) . g e t ( 0 ) ) . g e t C o o r d ( ) ;  
         a s s e r t   v . g e t X ( ) = = 1 . 0   a n d   v . g e t Y ( ) = = 0 . 0  
  
  
 i f   _ _ n a m e _ _   = =   " _ _ m a i n _ _ " :  
       #   t e s t H T M C o n s t r u c t u i o n ( ) ;  
       t e s t L a d d e r ( ) ;