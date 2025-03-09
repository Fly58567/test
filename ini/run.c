/************************************************************************
 ** Project      : Runner for CMS self test UUT site
 ** Filename     : run.c 
 ** Creator      : Mike Shu
 ** Date         : May 02, 2012
 ** Description  : This C source file is the Runner source code
 **
 ** Copyright (c) 2006--2012 Foxconn IND., Group. All Rights Reserved               
 **
 ** Version History 
 **
 ** Version      : 0.0.1
 ** Date         : May 02, 2012
 ** Revised by   : Mike Shu
 ** Description  : Alpha release
 **
 ************************************************************************/





#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<string.h>
#include<unistd.h>
#include<malloc.h>
#include<errno.h>

#include<netinet/in.h>
#include<sys/socket.h>

#include<sys/types.h>
#include<sys/wait.h>
#include <pthread.h>

#include <libxml/encoding.h>
#include <libxml/xmlwriter.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include<libxml/xmlreader.h>

#include "soapH.h"
#include "ServicesHttpBinding.nsmap"

#define MAX_DATA_SIZE 4098
#define BACKLOG 10
#define MAX_BUFF_LENGTH 32768

typedef struct _config_struc_
{
    char item_id[64];
    char proc_name[64];
    unsigned long dwFun_bit_map;
    unsigned char active;
}config_struc;

char *xml_hwchk_xml_path = "/usr/local/Foxconn/DiagCaptor/ini/HWCHK.xml";
char *xml_fun_select_xml_path = "/usr/local/Foxconn/DiagCaptor/ini/testscr.xml";
FILE *fphwcfg = NULL;
FILE *fpfunsel = NULL;
char cfgbuf[MAX_BUFF_LENGTH];
config_struc     ConfigSel[20];
int ItemAmount;
char BmcMac[32];
int  StartTestFlag = 0;

/*
** Function : Run ipmitool and get BMC MAC address,this will initial ipmi service firstly.
              Parse ipmitool print result
              
** Parameter: macadd  ==> return bmc mac address

** Return   : 0 returned if success, or 1 returned. 
*/

int get_bmcmac_address(char *macadd)
{
   char cmd[64];
   char bmcmac[32];
   FILE *fpbmc = NULL;
   char buffer[2048];
   char *pmac;
   int ret;
   int fileleng;
   //start ipmi service
   memset(cmd,0,sizeof(cmd));
   sprintf(cmd,"service ipmi start");
   ret = system(cmd);
   printf("server ipmi start return=%d\n",ret);
   
   memset(cmd,0,sizeof(cmd));
   sprintf(cmd,"ipmitool lan print > bmc.txt");
   ret = system(cmd);
   printf("system cmd return=%d\n",ret);
   fpbmc = fopen("bmc.txt","r");
   if(fpbmc == NULL)
   {
      printf("Can not open bmc.txt\n");
      return 1;
   }  
   memset(buffer,0,sizeof(buffer)); 
   //fgets(buffer,sizeof(buffer),fp);
    //Get file length
    fseek(fpbmc,0,SEEK_END);
    fileleng = ftell(fpbmc);
    printf("file length is:%d\n",fileleng);
     
   fseek(fpbmc,0,SEEK_SET);
   fread(buffer,fileleng,1,fpbmc);             
   fclose(fpbmc);
   printf("buffer=%s\n",buffer);
   pmac = strstr(buffer,"MAC Address");
   if(pmac == NULL)
   {
     printf("Not find flag MAC Address\n");
     return 1;
   }
   pmac = strstr(pmac,": ");
   memset(bmcmac,0,sizeof(bmcmac));
   strncpy(bmcmac,pmac+2,17);
   printf("bmc mac=%s\n",bmcmac);
   strncpy(macadd,bmcmac,17);  
   
   return 0;
}

/*
** Function : Parse Diagcaptor function select script file,and generate funciton config
              select structure
              
** Parameter: 

** Return   : 0 returned if success, or 1 returned,means fail. 
*/


int ParseFunctionSelect(void)
{
    /* xml area */
  
    const xmlChar *node_name;
    const xmlChar *attrvalue;
    const xmlChar *elemtvalue;
    
    //int  attriamount;
    xmlTextReaderPtr reader;
    int ret;
    int item_count;
    unsigned long dwbitmap;
    int i;


     //Clear parameter buffer
    for (i=0; i < 20; i++)
    {

       memset(&ConfigSel[i], 0 ,sizeof(config_struc));

    }  

    reader = xmlReaderForFile("/usr/local/Foxconn/DiagCaptor/ini/testscr.xml", NULL,0);
    if (reader != NULL) 
    {
        ret = xmlTextReaderRead(reader);
        while (ret == 1) 
        {
           //processNode(reader);            
           node_name = xmlTextReaderConstName(reader);
           if(xmlStrcmp(node_name,(xmlChar *)"ITEM_NUM") == 0)
           {
              xmlTextReaderRead(reader);
              printf("item_num=%s\n", xmlTextReaderConstValue(reader));
              break;
           }
                ret = xmlTextReaderRead(reader);
        }
        item_count = -1;
        ret = xmlTextReaderRead(reader);
        while (ret == 1) 
        {
                //processNode(reader);
                node_name = xmlTextReaderConstName(reader);
                if((xmlStrncmp(node_name,(xmlChar *)"FFT_ITEM",8) == 0)&&(xmlTextReaderNodeType(reader) == 1))
                {
                   //xmlTextReaderRead(reader);
                   //xmlTextReaderMoveToAttribute(reader,"item_id");
                   printf("\n");
                   item_count++;
                   //baseUrl = xmlTextReaderConstBaseUri(reader);
                   //printf("BaseURL=%s\n",baseUrl);
                   ConfigSel[item_count].dwFun_bit_map = 0;
                   node_name = xmlTextReaderConstName(reader);
                   printf("node_name=%s,Node_type=%d-------------\n", node_name,xmlTextReaderNodeType(reader));
                   
                   //Get item_id
                   attrvalue = xmlTextReaderGetAttribute(reader,(xmlChar*)"item_id");
                   strcpy(ConfigSel[item_count].item_id,(char *)attrvalue);
                   printf("item_id=%s\n", attrvalue);
                   
                   //Get proc_name
                   attrvalue = xmlTextReaderGetAttribute(reader,(xmlChar*)"proc_name");
                   strcpy(ConfigSel[item_count].proc_name,(char *)attrvalue);
                   printf("proc_name=%s\n", attrvalue);
                  
             
                  }
              
                /* Get function index bitmap */
                if((xmlStrncmp(node_name,(xmlChar *)"BITMAP",6) == 0)&&(xmlTextReaderNodeType(reader) == 1))
                {
             
                   node_name = xmlTextReaderConstName(reader);  
                   //set point to element value position
                   ret = xmlTextReaderRead(reader);           
                   elemtvalue = xmlTextReaderConstValue(reader);
                   sscanf((char *)elemtvalue,"%lx",&dwbitmap);
             
                   printf("Element_name=%s,Element_value=%s\n", node_name,elemtvalue);
                   printf("bitmap=0x%lx\n",dwbitmap);
              
                }

                /* Get function active status */
                if((xmlStrncmp(node_name,(xmlChar *)"ACTIVE",6) == 0)&&(xmlTextReaderNodeType(reader) == 1))
                {
             
                   node_name = xmlTextReaderConstName(reader);  
                   //set point to element value position
                   ret = xmlTextReaderRead(reader);           
                   elemtvalue = xmlTextReaderConstValue(reader);
                   if(xmlStrncmp(elemtvalue,(xmlChar *)"TRUE",4) == 0)
                   {
                       printf("test active\n");
                       ConfigSel[item_count].dwFun_bit_map = ConfigSel[item_count].dwFun_bit_map | dwbitmap;
                   }
                   printf("Element_name=%s,Element_value=%s\n", node_name,elemtvalue);
              
                }
                ret = xmlTextReaderRead(reader);
        }
        xmlFreeTextReader(reader);
            
      } 
      else
      {
         fprintf(stderr, "Unable to open %s\n", "testscr.xml");
         return 1;
         
      }

    //print function select 
    ItemAmount = item_count + 1;
    printf("ItemAmount=%d\n",ItemAmount);
    for(i = 0; i < ItemAmount; i++)
    {

      printf("item_id=%s,Fun_Select=0x%lx\n",ConfigSel[i].item_id,ConfigSel[i].dwFun_bit_map);

    }

    printf("parse function select complete!\n");
    return 0;
}

/*
   Function description:Wait for CMS Server send get system configuration requirement,
                        get system configuration in console mode,and response to CMS server.
   parameter: inmsg=message that need to check
  
   return:1=success,0=fail

*/

int UUT_Get_Config(char inmsg[])
{
	
	  int sockfd,new_fd;
	  struct sockaddr_in my_addr;
	  struct sockaddr_in client_addr;
	  int recvbytes;
    int sin_size;
    int fileleng = 0;
	  char buf[MAX_DATA_SIZE];    
	  int ret = 0;
    int on;
    int i;
       
	
    printf("Begin to receive get config message=%s\n",inmsg);
	  if((sockfd=socket(AF_INET,SOCK_STREAM,0))==-1)
	  {
	      perror("socket");
	      return 0;
	  }
        
	  my_addr.sin_family=AF_INET;
	  my_addr.sin_port=htons(3800);	
	  my_addr.sin_addr.s_addr=htonl(INADDR_ANY);
	  bzero(my_addr.sin_zero,8);
  
    //Set Port reuse function
    on = 1;
    if (setsockopt(sockfd,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on)) == -1)
    {

        perror("setsockopt");
        close(sockfd);
        return 0;
        
    }

	  if(bind(sockfd,(struct sockaddr *)&my_addr,sizeof(struct sockaddr))==-1)
	  {
	      perror("bind");
	      close(sockfd);
        return 0;
    }
    printf("bind pass\n");
	
	  if(listen(sockfd,BACKLOG)==-1)
	  {
	      perror("listen");
	      return 0;
	  }
    printf("listen pass\n");
    printf("wait for client link!\n");
        
	
    while(1)
	  {
	      sin_size=sizeof(struct sockaddr_in);	
	      printf("Prepara to accept to client link\n");
        if((new_fd=accept(sockfd,(struct sockaddr*)&client_addr,&sin_size))==-1)
	      {
	          perror("accept");
	          continue;
	      }
        printf("accept pass\n");	
	
	      memset(buf,0,MAX_DATA_SIZE);
        sprintf(buf,"Connect success,BmcMac=%s\n",BmcMac);
        if(send(new_fd,buf,strlen(buf),0)==-1)
	      {
	          perror("send");
	          close(new_fd);
            close(sockfd);
	          return 0;
	      }
        printf("send connect success complete!\n");

        //wait for client requirement
        memset(buf,0,MAX_DATA_SIZE);
	      if((recvbytes=recv(new_fd,buf,MAX_DATA_SIZE,0))==-1)
	      {
	          perror("recv");
            close(new_fd);
            close(sockfd);
	          return 0;
	      }
           
        /*
        printf("receive raw data=");
        for(i=0; i< recvbytes; i++)
        {
            printf("0x%02x ",buf[i]);
        }
        */
        //printf("\n");
	      //buf[recvbytes]='\0';
	      printf("Receive client request message=%s,length=%d\n",buf,recvbytes);
        //printf("standard msg=%s\n",inmsg);
	      //if(strcmp(buf,inmsg) == 0) 
        //wait for star_test
        if(strncmp(buf,"star_test",9) == 0)
        {
            StartTestFlag = 1;
            printf("start test flag=%d\n",StartTestFlag);
            //send start successful message
            memset(buf,0,MAX_DATA_SIZE);
            sprintf(buf,"Start test successful");
            if(send(new_fd,buf,strlen(buf),0)==-1)
	          {
	              perror("send start message");
	              close(new_fd);
                close(sockfd);
	              return 0;
	          }
	          //continue;
            //getchar();
        }
        
        //wait for get config
        else if(strncmp(buf,inmsg,strlen(inmsg)-1) == 0)
	      {       
            //recieve correct message
            fphwcfg = fopen("/usr/local/Foxconn/DiagCaptor/ini/HWCHK.xml","r");
            if(fphwcfg == NULL)
            {
                printf("File open error\n");
                close(new_fd);
                close(sockfd);
                return 0;         
            }
            //Get file length
            fseek(fphwcfg,0,SEEK_END);
            fileleng = ftell(fphwcfg);
            printf("file length is:%d\n",fileleng);
     
            //read file
            memset(cfgbuf,0,MAX_BUFF_LENGTH);
            fseek(fphwcfg,0,SEEK_SET);
            fread(cfgbuf,fileleng,1,fphwcfg);
            //close file handle
            fclose(fphwcfg);
               
            //send test config length string
            memset(buf,0,MAX_DATA_SIZE);
            sprintf(buf,"hwcfg_length=%d\n",fileleng);
            printf("buf=%s leng string length=%d\n",buf,strlen(buf));
            if (send(new_fd,buf,strlen(buf),0)==-1)
	          {
	              perror("send test config file length");
	              close(new_fd);
                close(sockfd);
	              return 0;
            }
            printf("send test config file length complete!\n");
        
	          //send test config context
            for (i = 0; i < fileleng; i = i + 4096)
            {
                memset(buf,0,MAX_DATA_SIZE);
                memcpy(buf,cfgbuf + i,4096);
                //buf[4096] = '\n';
                printf("\n\nbuf length=%d,content=%s\n",strlen(buf),buf);
                printf("\n\nbuf length=%d\n",strlen(buf));
                if (send(new_fd,buf,sizeof(buf),0)==-1)
	              {
	                  perror("send test config");
	                  close(new_fd);
                    close(sockfd);
	                  return 0;  //exit socket
                }
                
        
            }
            printf("send test config file complete!\n"); 
              
        }
        else
   	    {
            printf("Request is not correct,Wait for %s:\n",inmsg);
              
   	    }
  
    }//while
          
   
  	
    close(sockfd);
	  close(new_fd);
    return 1;	
}


void thread(void)
{
    char cfgmsg[64];
    memset(cfgmsg,0,sizeof(cfgmsg));
    sprintf(cfgmsg,"get_config\n");
    while(1)
    {
        if(UUT_Get_Config(cfgmsg)==1) //connect success
        {    
            printf("connect to CMS server and get test config pass\n");
    	  	
        }
        else
        {
            printf("connect to CMS server and get test config  fail\n");
            
    	  		
        }
    }

}

int get_fun_select()
{
    //send web service to CMS server and get function select file
  





    return 0;
}


/*

  return:1=success,0=fail

*/

int Star_test(char inmsg[])
{
	
	  int sockfd,new_fd;
	  struct sockaddr_in my_addr;
	  struct sockaddr_in client_addr;
	  int sin_size,recvbytes;
	  char buf[MAX_DATA_SIZE];    
	  int ret = 0;
    int on;
	
	  printf("Begin to receive function start message=%s\n",inmsg);
	  if ((sockfd=socket(AF_INET,SOCK_STREAM,0)) == -1)
	  {
	      perror("socket");
	      return ret;
	  }
        
    printf("Get function start socket pass\n");
	  my_addr.sin_family = AF_INET;
	  my_addr.sin_port = htons(3800);	
	  my_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	  bzero(my_addr.sin_zero,8);
        
    //Set socket reuse on
    on = 1;
    if (setsockopt(sockfd,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on)) == -1)
    {

        perror("setsockopt");
        close(sockfd);
        return ret;
    }

	  if (bind(sockfd,(struct sockaddr *)&my_addr,sizeof(struct sockaddr)) == -1)
	  {
	      perror("bind");
	      return ret;
    }
    printf("bind pass\n");
	
	  if (listen(sockfd,BACKLOG) == -1)
	  {
	      perror("listen");
     	  return ret;
	  }
    printf("listen pass\n");

	  while(1)
	  {
	      sin_size = sizeof(struct sockaddr_in);	
	      if((new_fd=accept(sockfd,(struct sockaddr*)&client_addr,&sin_size)) == -1)
	      {
	          perror("accept");
	          continue;
	      }
        printf("accept pass\n");
	      //printf("serve:Receive a new connection from :%s\n",(const char*)inet_ntoa(client_addr.sin_addr));
	
	      //Response connect successful message
        memset(buf,0,MAX_DATA_SIZE);
        sprintf(buf,"Connect success,BmcMac=%s\n",BmcMac);
        if (send(new_fd,buf,strlen(buf),0) == -1)	           
	      {
	          perror("send");
	          close(new_fd);
	          return ret;
	      }
        //receive "star_test"
        printf("Begin to receive start test message\n");
	      if((recvbytes=recv(new_fd,buf,MAX_DATA_SIZE,0))==-1)
	      {
	          perror("recv");
            close(new_fd);
	          return ret;
	      }
	      buf[recvbytes]='\0';
	      printf("Receive request message=");
	      printf("%s\n",buf);
        printf("standard msg=%s\n",inmsg);
	      if(strcmp(buf,inmsg) == 0) 
	      {       
            printf("receive correct message\n");
            getchar();
            ret = 1;
            break;   
        }
        else
   	    {
   		      printf("Request is not correct,Wait for %s:\n",inmsg);
   	    }
  
    }//while
	 
	  printf("Begin to receive start test message\n");
	  fpfunsel = fopen(xml_fun_select_xml_path,"w");        
    while(1)
    {
        memset(buf,0,sizeof(buf));
        if((recvbytes=recv(new_fd,buf,MAX_DATA_SIZE,0))==-1)
	      {
	          perror("recv");
            close(new_fd);
	          return ret;
	      }
           
        buf[4096] = 0;
        fprintf(fpfunsel,"%s",buf);
        printf("buf=%s\n",buf);
	      if(strstr(buf,"/DiagproCaptor_Root") != NULL)
        {
            break;
        }
        //getchar();  
        
    }  

    fclose(fpfunsel);        
    close(sockfd);
	  close(new_fd);
        
        
    return ret;	
	
}




int main()
{
  
    char * argv[4]; //={"ls,""-al",0};
    char  netmsg[64];
    char program[64];
    memset(netmsg,0,64);
    sprintf(netmsg,"get_config\n");
    int i,j,rtn;
    char fun_sel_buf[32];
    unsigned long dwtemp;
    int ret;
    char cmd[64];
    pthread_t id;
    pthread_attr_t attr;
  
    //const char web_service_server[] = "http://10.141.104.195:8000";
    const char web_service_server[] = "http://10.141.104.137/ITMgr/Interface/Services";
    struct soap soap;
    double a,b,result;
    struct _ns1__getName StrName;
    struct _ns1__getNameResponse StrNameRes;


    memset(BmcMac,0,sizeof(BmcMac));
    get_bmcmac_address(BmcMac);
    
    //Create system configuration file
    //hwchk test
    if (fork() == 0) //children process
    {
        printf("child id=%d\n",getpid());
        printf("parent id=%d\n",getppid());
        argv[0] = "./cputest";
     	  argv[1] = "-e";
     	  argv[2] = "0x1ff";
     	  argv[3] = 0;
     	  //execvp(argv[0],argv);
     	  execlp( "./hwchktest", "./hwchktest","-c",NULL );
        // 如果exec函数返回，表明没有正常执行命令，打印错误信息
        perror( "./hwchktest" );
        exit( errno );

     	      
    }
    else
    {
        wait(&rtn);
        printf( " child process return %d\n", rtn );
        printf("child id=%d\n",getpid());
        printf("parent id=%d\n",getppid());
        printf("hwchk test complete!\n");

    }       
    //getchar();

    memset(cmd,0,sizeof(cmd));
    sprintf(cmd,"service iptables stop");
    ret = system(cmd);
    printf("service iptables start return=%d\n",ret);
   
    /*  
    //Wait for Get system configuration requirement and response system config
    while(1)
    {
        if(UUT_Get_Config(netmsg)==1) //connect success
        {    
      
            printf("connect to CMS server and get test config pass\n");
    	  	
        }
        else
        {
            printf("connect to CMS server and get test config  fail\n");
            //return 1;    	  		
    	  		
        }
    }*/
    pthread_attr_init(&attr);
    ret = pthread_create(&id,&attr,(void*) thread,NULL);
    if(ret != 0)
    {
        printf("Create thread error\n");
        exit(1);
    }
    //pthread_join(id,NULL);
    //return 1;
    
    /*
    //Star function test  
    memset(netmsg,0,64);
    sprintf(netmsg,"star_test");
    //Mike shu debug
    Star_test(netmsg);
    return 1;
    //end of debug
    */
    //if(Star_test(netmsg)==1)
    while(1)
    {
        if(StartTestFlag == 1)
        {
            ParseFunctionSelect();
      
            //printf("debug1\n");
       
            for(i=0;i< ItemAmount;i++)
            { 
                ////if(fork() == 0) //children process
                ////{
                memset(fun_sel_buf,0,sizeof(fun_sel_buf));
                memset(program,0,sizeof(program));
                sprintf(fun_sel_buf,"0x%lx",ConfigSel[i].dwFun_bit_map);
                printf("fun_name=%s,proc_name=%s,fun_bitmap=%s\n",ConfigSel[i].item_id,ConfigSel[i].proc_name,fun_sel_buf);
                sprintf(program,"./%s",ConfigSel[i].proc_name);
                //printf("program name=%s\n",program);
        
                for(j = 0; j < 32; j++)
                {
                    if(((ConfigSel[i].dwFun_bit_map  >> j) & 0x01) == 0x01)
                    {
                        dwtemp = ConfigSel[i].dwFun_bit_map & (1 << j);
                        sprintf(fun_sel_buf,"0x%lx",dwtemp);
                        //getchar();
                        if(fork() == 0)
                        {
                            printf("fun_name=%s,proc_name=%s,fun_unit_bitmap=%s\n",ConfigSel[i].item_id,ConfigSel[i].proc_name,fun_sel_buf);
                            printf("program name=%s\n",program);
                            execlp( program, program,"-e",fun_sel_buf,NULL );
                            // 如果exec函数返回，表明没有正常执行命令，打印错误信息
                            perror( program );
                            exit( errno );
                        }
                        else
                        {
                            wait(&rtn);
                            printf( " child process %s,unit=%d,return =0x%lx\n",ConfigSel[i].proc_name, j+1,rtn );
                            a = j;
                            b = j+1;
                            /*
                            soap_init1(&soap,SOAP_XML_INDENT);
                            //soap_call_ns__add(&soap, web_service_server, "", a, b, &result);
                            soap_init1(&soap, SOAP_XML_INDENT); 
                            StrName.name = (char *)malloc(64); 
                            memset(StrName.name,0,64);
                            //sprintf(StrName.name,"debug test");
                            if(rtn == 0)
                            {
                                sprintf(StrName.name,"%s,unit%d test pass!\n",ConfigSel[i].item_id,j+1); 
                            }
                            else
                            {
                                sprintf(StrName.name,"%s,unit%d test fail!\n",ConfigSel[i].item_id,j+1); 
                            }
                           
                           soap_call___ns1__getName(&soap, web_service_server,"",&StrName,&StrNameRes);
                          if (soap.error)
                          { 
                           free(StrName.name);
                             soap_print_fault(&soap, stderr);
                              exit(1);
                         }
                         else
                         {
                           printf("soap result = %s\n", StrNameRes.out);
                           free(StrName.name);
                              //close web service resource
                              soap_destroy(&soap);
  	                    soap_end(&soap);
  	                   soap_done(&soap);
                         }
                         */
               
              
                            printf("%s,unit%d test complete!\n",ConfigSel[i].item_id,j+1); 
              
                        } //end of else
                     }//end of unit select
                    
                }//end of for(j = 0; j < 32; j++)       
     
      
            } //end of for(i=0;i< ItemAmount;i++)
        printf("All test item pass\n");
        StartTestFlag = 0;
        } //if(StartTestFlag == 1)
    } //end of while loop
    pthread_join(id,NULL); //wait for children process complete

    return 1;
 }

