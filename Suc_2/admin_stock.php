<?php
include_once "_core.php";
include('num2letras.php');
function initial()
{
  $title = "Consultar Existencias";
  $_PAGE = array();
  $_PAGE ['title'] = $title;
  $_PAGE ['links'] = null;
  $_PAGE ['links'] .= '<link href="css/bootstrap.min.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="font-awesome/css/font-awesome.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/plugins/iCheck/custom.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/plugins/select2/select2.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/plugins/toastr/toastr.min.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/plugins/datapicker/datepicker3.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/animate.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/style.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/plugins/sweetalert/sweetalert.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/style2.css" rel="stylesheet">';
  $_PAGE ['links'] .= '<link href="css/pagination.css" rel="stylesheet">';
  include_once "header.php";
  include_once "main_menu.php";
  include('Pagination.php');
  //permiso del script
  $id_sucursal=$_SESSION["id_sucursal"];
  $id_user=$_SESSION["id_usuario"];
  $admin=$_SESSION["admin"];

  $uri = $_SERVER['SCRIPT_NAME'];
  $filename=get_name_script($uri);
  $links=permission_usr($id_user, $filename);
  ?>
  <div class="wrapper wrapper-content  animated fadeInRight">
    <div class="row">
      <div class="col-lg-12">
        <div class="ibox ">
          <?php
          //permiso del script
          if ($links!='NOT' || $admin=='1') {
            ?>
            <div class="ibox-content">
              <?php
              //VENTA
              $fecha_actual=date("Y-m-d"); ?>
              <div class="widget">
                <div class="row">
                  <div class="col-md-12">
                    <div class="row">
                      <div class="widget-header">
                        <div class="row">
                          <div class="col-md-4">&nbsp;&nbsp;
                            <i class="fa fa-th-list"> </i>
                            <h3 class="text-navy" id='title-table'><?php echo $title; ?></h3>
                          </div>
                          <div class="form-group col-md-4">
                            <!--label>Limite Busqueda&nbsp;
                            <input type="text"  class='form-control input_header_panel'  id="limite" value=400 /-->
                          </div>

                          <div class="form-group col-md-3">
                            <label>Reg. Encontrados&nbsp;
                              <input type="text"  class='form-control input_header_panel' id='reg_count' value=0 readOnly /></label>
                            </div>
                          </div>
                        </div>
                        <div class="widget-content">
                          <div class="row">
                            <div class="col-md-4">
                              <div class="form-group">
                                <input type="text" id="keywords" class='form-control' placeholder="Descripción">
                              </div>
                            </div>
                            <div class="col-md-4">
                              <div class="form-group">
                                <input type="text" id="barcode" class='form-control' placeholder="Codigo de barra">
                              </div>
                            </div>
                            <div class="col-md-4">
                              <div class="form-group">
                                <select class="form-control select" id='ubicacion'>
                                  <option value="">CONSOLIDADO</option>
                                  <?php
                                  $sql = _query("SELECT * FROM ubicacion WHERE id_sucursal='$id_sucursal' ORDER BY descripcion ASC");
                                  while($row = _fetch_array($sql))
                                  {
                                    echo "<option value='".$row["id_ubicacion"]."'>".$row["descripcion"]."</option>";
                                  }
                                  ?>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class='row' id='encabezado_buscador'>
                            <div class="col-md-4">
                              <div class="form-group">
                                <label>&nbsp;Ordenar </label>
                                <select id="sortBy" onchange="searchFilter()">
                                  <option value="asc">Ascendente</option>
                                  <option value="desc">Descendente</option>
                                </select>
                              </div>
                            </div>
                            <div class="col-md-3">&nbsp;&nbsp;</div>
                            <div class="col-md-3">&nbsp;&nbsp;</div>
                            <div class="col-md-2 pull-right">
                              <div class="form-group">
                                <label>Registros </label>
                                <select id="records" onchange="searchFilter()">
                                  <option value="5">5</option>
                                  <option value="10" selected>10</option>
                                  <option value="25">25</option>
                                  <option value="50">50</option>
                                  <option value="100">100</option>
                                  <option value="200">200</option>
                                  <option value="500">500</option>
                                </select>
                              </div>
                            </div>

                          </div>
                          <div class="row">
                            <div class="loading-overlay col-md-6">
                              <div class="overlay-content text-warning" id='reg_count0'>Cargando.....</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div  class='widget-content' id="content">
                      <div class="row">
                        <div class="col-md-12">
                          <table class="table table-bordered" id='loadtable'>
                            <thead>
                              <tr>
                                <th class="text-success col-lg-1">Código</th>
                                <th class="text-success col-lg-4">Producto</th>
                                <th class="text-success col-lg-2">Categoría</th>
                                <th class="text-success col-lg-2">Presentación</th>
                                <th class="text-success col-lg-1">Descripción</th>
                                <th class="text-success col-lg-1">Precio</th>
                                <th class="text-success col-lg-1">Existencia</th>
                              </tr>
                            </thead>
                            <tbody id="mostrardatos">
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div id="paginador"></div>
                  <input type='hidden' name='totalfactura' id='totalfactura' value='0'>
                  <input type='hidden' name='urlprocess' id='urlprocess'value="<?php echo $filename; ?>">
                  <input type="hidden" name="process" id="process" value="insert">
                </div>
              </div>
              <?php
            } //permiso del script
            else
            {
              echo "<div></div><br><br><div class='alert alert-warning'>No tiene permiso para este modulo.</div>";
            }
            ?>
          </div>
        </div>
      </div>
    </div>
    <?php
    include_once("footer.php");
    echo "<script src='js/plugins/arrowtable/arrow-table.js'></script>";
    echo "<script src='js/funciones/funciones_stock.js'></script>";
  }
  function traerdatos()
  {
    $start = !empty($_POST['page'])?$_POST['page']:0;
    $limit =$_POST['records'];
    $sortBy = $_POST['sortBy'];
    $keywords = $_POST['keywords'];

    $id_sucursal= $_SESSION['id_sucursal'];
    $id_ubicacion= $_POST['id_ubicacion'];
    $barcode= $_POST['barcode'];

    $sqlJoined="  SELECT pr.id_producto,pr.descripcion, pr.barcode, c.nombre_cat as cat, SUM(su.cantidad) as cantidad
    FROM producto AS pr LEFT JOIN categoria AS c ON c.id_categoria=pr.id_categoria LEFT JOIN stock_ubicacion AS su ON pr.id_producto = su.id_producto";

    $sqlParcial= get_sql($start,$limit,$keywords,$sortBy, $id_ubicacion, $barcode);
    $orderBy=" ORDER BY pr.descripcion";
    $groupBy=" GROUP BY pr.id_producto";
    $limitSQL= " LIMIT $start,$limit ";
    $sql_final= $sqlJoined." ".$sqlParcial." ".$groupBy." ".$orderBy." ".$limitSQL;

    //echo $sql_final;
    $query = _query($sql_final);
    //echo $sql_final;
    $num_rows = _num_rows($query);
    $filas=0;
    if ($num_rows > 0)
    {
      while ($row = _fetch_array($query))
      {
        $id_producto = $row['id_producto'];
        $descripcion=$row["descripcion"];
        $cat = $row['cat'];
        $barcode = $row['barcode'];
        $existencias = $row['cantidad'];
        /*$estante=$row['estante'];
        $posicion=$row['posicion'];*/

        $estante='NO ASIGNADO';
        $posicion='';

        /*if ($estante==''&&$posicion=='') {
          $estante='NO ASIGNADO';
          $posicion='';
        }
        else {
          $posicion='POSICIÓN '.$posicion;
        }*/
        $sql_pres = _query("SELECT pp.*, p.nombre as descripcion_pr FROM presentacion_producto as pp, presentacion as p WHERE pp.id_presentacion=p.id_presentacion AND pp.id_producto='$id_producto' ORDER BY pp.unidad DESC");
        $npres = _num_rows($sql_pres);
        ?>
        <tr>
          <td rowspan="<?php echo $npres; ?>" style="vertical-align:middle;"><h5><?php echo $barcode; ?></h5></td>
          <td rowspan="<?php echo $npres; ?>" style="vertical-align:middle;"><?php echo $descripcion; ?></td>
          <td rowspan="<?php echo $npres; ?>" style="vertical-align:middle;"><?php echo $cat; ?></td>
          <?php
          $exis = 0;
          $n=0;
          $i=1;
          while ($rowb = _fetch_array($sql_pres))
          {
            $unidad = $rowb["unidad"];
            $costo = $rowb["costo"];
            $precio = $rowb["precio"];

            $descripcion_pr = $rowb["descripcion"];
            $presentacion = $rowb["descripcion_pr"];

              if($existencias >= $unidad)
              {
                if ($existencias>0&& $npres == $i) {
                  // code...
                  $exis = round($existencias/$unidad,4);
                }
                else {
                  $exis = intdiv($existencias, $unidad);
                  $existencias = $existencias - ($exis *$unidad);
                }
              }
              else
              {
                if ($existencias>0&& $npres == $i) {
                  // code...
                  $exis = round($existencias/$unidad,4);
                }
                else {
                  // code...

                  $exis =  0;
                }
              }

            $i++;

            if($n>0)
            {
                echo "<tr><td colspan='3'>";
            }
            ?>
            <td><?php echo $presentacion; ?></td>
            <td><?php echo $descripcion_pr; ?></td>

            <td><?php echo $precio; ?></td>
            <td><?php echo $exis; ?></td>
            </tr>
            <?php
            $filas+=1;
          }
        }
      }
    }
    function traerpaginador()
    {
      $start = !empty($_POST['page'])?$_POST['page']:0;
      $limit =$_POST['records'];
      $keywords = $_POST['keywords'];
      $sortBy = $_POST['sortBy'];

      $id_sucursal= $_SESSION['id_sucursal'];
      $id_ubicacion= $_POST['id_ubicacion'];
      $barcode= $_POST['barcode'];
      $limite=50;
      $whereSQL =$andSQL =  $orderSQL = '';
      if(isset($_POST['page']))
      {
        include('Pagination.php');
        $sqlParcial=get_sql($start,$limit,$keywords,$sortBy,$id_ubicacion,$barcode);
        $sql1="SELECT COUNT(DISTINCT(pr.id_producto)) as numRecords  FROM producto AS pr LEFT JOIN stock_ubicacion AS su ON pr.id_producto = su.id_producto";
        if($id_ubicacion !="")
        {
          $sql1="SELECT COUNT(DISTINCT(pr.id_producto)) as numRecords  FROM producto AS pr LEFT JOIN stock_ubicacion AS su ON pr.id_producto = su.id_producto";
        }
        $sql_numrows=$sql1.$sqlParcial;
        //echo $sql_numrows;
        $queryNum = _query($sql_numrows);
        $resultNum = _fetch_array($queryNum);
        $rowCount = $resultNum['numRecords'];

        $pagConfig = array(
          'currentPage' => $start,
          'totalRows' => $rowCount,
          'perPage' => $limit,
          'link_func' => 'searchFilter'
        );
        $pagination =  new Pagination($pagConfig);
        echo $pagination->createLinks();
        echo '<input type="hidden" id="cuantos_reg"  value="'.$rowCount.'">';
      }
    }
    function get_sql($start,$limit,$keywords,$sortBy,$id_ubicacion,$barcode)
    {
      $andSQL='';
      $id_sucursal= $_SESSION['id_sucursal'];
      $whereSQL=" WHERE pr.estado=1 ";
      if($id_ubicacion != "")
      {
        $whereSQL=" WHERE pr.estado=1 AND su.id_ubicacion='$id_ubicacion'
        ";
      }
      $keywords=trim($keywords);
      $barcode=trim($barcode);
      if($barcode!="")
      {
        $andSQL.= " AND  pr.barcode LIKE '%".$barcode."%'";
      }
      if($keywords!="")
      {
        $andSQL.=" AND pr.descripcion LIKE '%".$keywords."%'";
      }
      $sql_parcial=$whereSQL.$andSQL;
      return $sql_parcial;
    }
    if (!isset($_REQUEST['process']))
    {
      initial();
    }
    if (isset($_REQUEST['process']))
    {
      switch ($_REQUEST['process'])
      {
        case 'insert':
        insertar();
        break;
        case 'traerdatos':
        traerdatos();
        break;
        case 'traerpaginador':
        traerpaginador();
        break;
      }
    }
    ?>
