# Essas são anotações do curso de S3 - Modulo: Security Access Control

    - Cross Account Access:
        * Cross account access is when one AWS account grants permissions to its resources to another
        AWS account
        * Root Account A grants permissions via a bucket policy to Account B
        * Account A administrator grants cross account permissions, via a bucket policy, to Account B
        to perform a specific task
        * Account B administrator delegates permissions to a user within its account via a user policy
        * The user in Account B then verifies permissions by accessing an object in the bucket owned by Account A

            > A good use case for cross account access is in the case of logging or billing.
            
    - Which Policies Can I Use?

                When applying permissions to S3 resources you can use 
                either resource policies, 
                user policies or both!

    - Evaluating Policies: Bucket Operations:

                If the user and the bucket all belong to the same AWS account then all
                policies are evaluated at the same time

                If access is granted via one policy and denied via another, deny wins.
            
                The users account must first grant them access to the bucket  via user policy

                The bucket owner must then grant them access

                In most cases the preferred method of grating access is either via a User Policy or a
                Bucket Policy as these are able to grant much finer permissions than ACL's. The choice of
                which to use is really down to personal preference.
    Tradução:   (Na maioria dos casos, o método preferencial de conceder acesso é pormeio de uma Política de
                usuário ou Política de intervalo, pois eles podem conceder permissões muito mais refinadas do
                que as ACLs. A escolha de qual usar é realmente uma questão de preferência pessoal.)

             -> However there are situations in which certain policies must be used
                * ACL's 
                    >> To manage access to objects not owned by the bucket owner 
                    >> To manage access to individual objects when permissions must vary between objetcs
                    >> To grant permission to the "S3 Log Delivery Group" on a bucket 
        RECAP: 
             -> TWO TYPE OF POLICIES

                * Resource based policies consisting of Bucket policies and Access Cotrol Lists
                * User Policies

             -> When apply permissions you can use resource policies, user policiess or both 
             -> S3 evaluaates ALL policies to determine if access is granted
                -> The order of the policy evaluation depends on the ownership of the resources
             -> Bucket % User policies are the preferred method of grating access but there are certain use cases where certain
                policies must be used. 
            



                
